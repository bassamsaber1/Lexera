from __future__ import annotations

from datetime import datetime, timezone
from math import ceil
from typing import Any

import streamlit as st

from services.ai_client import LexeraAIClient
from services.auth import verify_password
from services.lawegypt_client import LawEgyptClient
from services.storage import JsonStorage
from services.user_store import ROLE_PERMISSIONS, UserStore

MY_FILES_PATH = "data/my_files.json"
ACTIVITY_PATH = "data/activity_log.json"

TOKEN_COSTS = {
    "contracts.analyze": 150,
    "cases.analyze": 170,
    "memo.create": 200,
    "chat.open": 120,
}


def _storage(path: str) -> JsonStorage:
    return JsonStorage(path)


def _log_activity(actor: str, action: str, metadata: dict[str, Any] | None = None) -> None:
    store = _storage(ACTIVITY_PATH)
    logs = store.load(default=[])
    logs.append(
        {
            "at": datetime.now(timezone.utc).isoformat(),
            "actor": actor,
            "action": action,
            "metadata": metadata or {},
        }
    )
    store.save(logs[-500:])


def _load_my_files() -> list[dict[str, Any]]:
    return _storage(MY_FILES_PATH).load(default=[])


def _save_my_files(items: list[dict[str, Any]]) -> None:
    _storage(MY_FILES_PATH).save(items)


def _remaining_tokens(user: dict[str, Any]) -> int:
    return max(0, int(user.get("token_quota", 0)) - int(user.get("token_used", 0)))


def _charge_tokens(users: UserStore, user_id: str, cost: int) -> tuple[bool, str]:
    target = users.find_by_id(user_id)
    if not target:
        return False, "المستخدم غير موجود"

    if _remaining_tokens(target) < cost:
        return False, "لا يوجد رصيد توكنات كافي"

    ok, msg = users.update_user(
        user_id,
        lambda u: {
            **u,
            "token_used": int(u.get("token_used", 0)) + cost,
        },
    )
    return ok, msg


def _auth_screen(users: UserStore) -> None:
    st.title("Lexera – Egypt Legal System")
    st.caption("منصة بحث وتحليل قانوني داخلي فقط. لا تقدم استشارات قانونية أو فتاوى.")

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("اسم المستخدم")
        password = st.text_input("كلمة المرور", type="password")
        submitted = st.form_submit_button("تسجيل الدخول", type="primary")

    if submitted:
        user = users.find_by_username(username)
        if not user:
            st.error("بيانات الدخول غير صحيحة")
            return
        if not user.get("is_active", False):
            st.error("الحساب غير مفعل")
            return
        if not verify_password(password, user["password_hash"], user["password_salt"]):
            st.error("بيانات الدخول غير صحيحة")
            return
        st.session_state.user_id = user["id"]
        _log_activity(user["username"], "LOGIN")
        st.rerun()


def _run_ai_action(
    users: UserStore,
    ai: LexeraAIClient,
    user: dict[str, Any],
    permission: str,
    prompt: str,
    system_instruction: str,
) -> None:
    if not users.can(user, permission):
        st.error("ليس لديك صلاحية لهذا القسم")
        return

    cost = TOKEN_COSTS[permission]
    if _remaining_tokens(user) < cost:
        st.error("تم تجاوز الرصيد المتاح. برجاء التواصل مع الإدارة لزيادة التوكنات.")
        return

    if not ai.configured:
        st.error("لم يتم ضبط مفاتيح LEXERA_API في البيئة.")
        return

    if not prompt.strip():
        st.warning("أدخل النص أولاً")
        return

    with st.spinner("جاري التحليل..."):
        try:
            answer = ai.chat(system_prompt=system_instruction, user_prompt=prompt)
        except Exception as error:  # noqa: BLE001
            st.error(f"تعذر تنفيذ الطلب: {error}")
            return

    charged, msg = _charge_tokens(users, user["id"], cost)
    if not charged:
        st.error(msg)
        return

    _log_activity(user["username"], f"AI_ACTION:{permission}", {"cost": cost})
    st.success(f"تم خصم {cost} توكن")
    st.markdown("#### النتيجة")
    st.write(answer)


def _contracts_page(users: UserStore, ai: LexeraAIClient, user: dict[str, Any]) -> None:
    st.subheader("قسم تحليل عقود")
    txt = st.text_area("ألصق نص العقد", height=220)
    if st.button("تحليل العقد", type="primary"):
        _run_ai_action(
            users,
            ai,
            user,
            "contracts.analyze",
            txt,
            "حلل العقد تحليلاً بحثياً: المخاطر، البنود غير الواضحة، واقتراحات تدقيق دون إعطاء نصيحة قانونية ملزمة.",
        )


def _cases_page(users: UserStore, ai: LexeraAIClient, user: dict[str, Any]) -> None:
    st.subheader("قسم تحليل قضايا ودفوع")
    txt = st.text_area("اكتب ملخص الوقائع والطلبات والدفوع", height=220)
    if st.button("تحليل القضية والدفوع", type="primary"):
        _run_ai_action(
            users,
            ai,
            user,
            "cases.analyze",
            txt,
            "قم بتحليل بحثي للقضية: الوقائع، عناصر الإثبات، الدفوع المحتملة، نقاط القوة والضعف، دون تقديم فتوى أو قرار نهائي.",
        )


def _memo_page(users: UserStore, ai: LexeraAIClient, user: dict[str, Any]) -> None:
    st.subheader("قسم إنشاء مذكرة دفاع")
    txt = st.text_area("أدخل الوقائع القانونية لإنشاء مسودة مذكرة دفاع", height=220)
    if st.button("إنشاء مسودة", type="primary"):
        _run_ai_action(
            users,
            ai,
            user,
            "memo.create",
            txt,
            "أنشئ مسودة مذكرة دفاع منظمة (الوقائع، الدفوع، الطلبات) بصياغة عربية مهنية مع الإشارة أنها مسودة بحثية غير ملزمة.",
        )


def _search_page(users: UserStore, client: LawEgyptClient, user: dict[str, Any]) -> None:
    st.subheader("قسم البحث في lawegypt.net")
    if not users.can(user, "search.use"):
        st.error("ليس لديك صلاحية")
        return

    if "search_results" not in st.session_state:
        st.session_state.search_results = []

    query = st.text_input("ابحث بالكلمة أو اسم القانون")
    cols = st.columns([2, 1])
    if cols[0].button("بحث", type="primary", use_container_width=True):
        with st.spinner("جاري البحث..."):
            try:
                st.session_state.search_results = client.search(query.strip()) if query.strip() else []
            except Exception as error:  # noqa: BLE001
                st.error(f"تعذر البحث: {error}")
    cols[1].link_button("فتح الموقع", "https://lawegypt.net", use_container_width=True)

    for idx, result in enumerate(st.session_state.search_results):
        with st.container(border=True):
            st.markdown(f"**{result.title}**")
            st.caption(result.url)
            st.write(result.snippet or "-")
            if st.button("حفظ في ملفاتي", key=f"save_{idx}"):
                files = _load_my_files()
                if any(row["url"] == result.url and row.get("user_id") == user["id"] for row in files):
                    st.info("المادة محفوظة بالفعل")
                else:
                    try:
                        content = client.fetch_article_text(result.url)
                    except Exception:
                        content = ""
                    files.append(
                        {
                            "user_id": user["id"],
                            "title": result.title,
                            "url": result.url,
                            "snippet": result.snippet,
                            "content": content,
                            "saved_at": datetime.now(timezone.utc).isoformat(),
                        }
                    )
                    _save_my_files(files)
                    _log_activity(user["username"], "SAVE_MY_FILE", {"url": result.url})
                    st.success("تم الحفظ في ملفاتي")

    st.markdown("### ملفاتي")
    my_files = [f for f in _load_my_files() if f.get("user_id") == user["id"]]
    if not my_files:
        st.info("لا توجد مواد محفوظة")
    for idx, item in enumerate(reversed(my_files), start=1):
        with st.expander(f"{idx}. {item['title']}"):
            st.caption(item["saved_at"])
            st.write(item.get("snippet") or "-")
            st.link_button("المصدر", item["url"], key=f"src_{idx}")
            if item.get("content"):
                st.text_area("النص", value=item["content"], height=200, disabled=True, key=f"cont_{idx}")


def _chat_page(users: UserStore, ai: LexeraAIClient, user: dict[str, Any]) -> None:
    st.subheader("قسم شات مفتوح")
    if not users.can(user, "chat.open"):
        st.error("ليس لديك صلاحية")
        return

    prompt = st.text_area("اكتب سؤالك البحثي", height=180)
    if st.button("إرسال", type="primary"):
        _run_ai_action(
            users,
            ai,
            user,
            "chat.open",
            prompt,
            "أجب كمساعد بحث قانوني مصري. لا تقدم نصيحة قانونية أو فتوى. اذكر أن الرد لأغراض بحثية.",
        )


def _admin_dashboard(users: UserStore, current_user: dict[str, Any]) -> None:
    st.subheader("لوحة الإدارة")
    if not users.can(current_user, "admin.users.manage"):
        st.error("صلاحيات Admin فقط")
        return

    all_users = users.list_users()
    total_quota = sum(int(u.get("token_quota", 0)) for u in all_users)
    total_used = sum(int(u.get("token_used", 0)) for u in all_users)

    c1, c2, c3 = st.columns(3)
    c1.metric("إجمالي المستخدمين", len(all_users))
    c2.metric("إجمالي التوكنات", total_quota)
    c3.metric("المستخدم", total_used)

    st.markdown("### إضافة مستخدم")
    with st.form("add_user"):
        username = st.text_input("Username")
        full_name = st.text_input("الاسم الكامل")
        password = st.text_input("كلمة المرور", type="password")
        role = st.selectbox("الدور", ["admin", "reviewer", "viewer"])
        quota = st.number_input("Token Quota", min_value=0, value=5000, step=1000)
        add_btn = st.form_submit_button("إضافة")

    if add_btn:
        ok, msg = users.add_user(username, full_name, password, role, int(quota))
        if ok:
            _log_activity(current_user["username"], "ADMIN_ADD_USER", {"username": username})
            st.success(msg)
            st.rerun()
        else:
            st.error(msg)

    st.markdown("### إدارة المستخدمين")
    for user in all_users:
        with st.container(border=True):
            rem = _remaining_tokens(user)
            st.markdown(
                f"**{user['full_name']}** (`{user['username']}`) - role: `{user['role']}` - "
                f"active: `{user['is_active']}` - remaining: `{rem}`"
            )

            col1, col2, col3, col4 = st.columns(4)
            toggle_label = "إلغاء التفعيل" if user["is_active"] else "تفعيل"
            if col1.button(toggle_label, key=f"tog_{user['id']}"):
                ok, msg = users.update_user(user["id"], lambda u: {**u, "is_active": not u["is_active"]})
                if ok:
                    _log_activity(current_user["username"], "ADMIN_TOGGLE_USER", {"user": user["username"]})
                    st.success("تم التحديث")
                    st.rerun()
                else:
                    st.error(msg)

            add_tokens = int(col2.number_input("+Tokens", min_value=0, value=0, key=f"tok_{user['id']}"))
            if col2.button("إضافة توكنات", key=f"tok_btn_{user['id']}"):
                ok, msg = users.update_user(
                    user["id"],
                    lambda u: {**u, "token_quota": int(u.get("token_quota", 0)) + add_tokens},
                )
                if ok:
                    _log_activity(current_user["username"], "ADMIN_ADD_TOKENS", {"user": user["username"], "tokens": add_tokens})
                    st.success("تمت إضافة التوكنات")
                    st.rerun()
                else:
                    st.error(msg)

            note = col3.text_input("ملاحظة مخالفة", key=f"vio_{user['id']}")
            if col3.button("حفظ المخالفة", key=f"vio_btn_{user['id']}"):
                ok, msg = users.update_user(
                    user["id"],
                    lambda u: {**u, "violations": [*u.get("violations", []), note] if note else u.get("violations", [])},
                )
                if ok:
                    _log_activity(current_user["username"], "ADMIN_VIOLATION_NOTE", {"user": user["username"]})
                    st.success("تم الحفظ")
                    st.rerun()
                else:
                    st.error(msg)

            if col4.button("حذف المستخدم", key=f"del_{user['id']}"):
                ok, msg = users.delete_user(user["id"])
                if ok:
                    _log_activity(current_user["username"], "ADMIN_DELETE_USER", {"user": user["username"]})
                    st.success("تم الحذف")
                    st.rerun()
                else:
                    st.error(msg)

            with st.expander("صلاحيات إضافية (Override)"):
                role_perms = ROLE_PERMISSIONS.get(user["role"], set())
                for perm in sorted({*TOKEN_COSTS.keys(), "search.use", "admin.users.manage"}):
                    inherited = perm in role_perms
                    current = user.get("permissions_override", {}).get(perm)
                    label = f"{perm} (role default={inherited})"
                    new_val = st.selectbox(
                        label,
                        options=["inherit", "allow", "deny"],
                        index=0 if current is None else (1 if current else 2),
                        key=f"ovr_{user['id']}_{perm}",
                    )
                    if st.button(f"حفظ {perm}", key=f"save_perm_{user['id']}_{perm}"):
                        def _updater(u: dict[str, Any]) -> dict[str, Any]:
                            ovr = dict(u.get("permissions_override", {}))
                            if new_val == "inherit":
                                ovr.pop(perm, None)
                            else:
                                ovr[perm] = new_val == "allow"
                            return {**u, "permissions_override": ovr}

                        ok, msg = users.update_user(user["id"], _updater)
                        if ok:
                            _log_activity(current_user["username"], "ADMIN_PERMISSION_OVERRIDE", {"user": user["username"], "perm": perm})
                            st.success("تم تحديث الصلاحية")
                            st.rerun()
                        else:
                            st.error(msg)


def main() -> None:
    st.set_page_config(page_title="Lexera Egypt", page_icon="⚖️", layout="wide")
    st.markdown(
        """
        <style>
            .stApp {background: linear-gradient(180deg,#0f172a 0%,#111827 100%); color: #f8fafc;}
            .stMarkdown, .stText, .stCaption, h1,h2,h3 {color: #f8fafc !important;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    users = UserStore()
    ai = LexeraAIClient()
    law_client = LawEgyptClient()

    if "user_id" not in st.session_state:
        _auth_screen(users)
        return

    user = users.find_by_id(st.session_state.user_id)
    if not user or not user.get("is_active", False):
        st.session_state.pop("user_id", None)
        st.warning("انتهت الجلسة")
        st.rerun()

    st.sidebar.title("Lexera Control")
    st.sidebar.caption(f"{user['full_name']} | {user['role']}")
    st.sidebar.metric("Remaining Tokens", _remaining_tokens(user))
    st.sidebar.caption("This system does not provide legal advice or fatwas.")

    page = st.sidebar.radio(
        "الأقسام",
        [
            "تحليل عقود",
            "تحليل قضايا ودفوع",
            "إنشاء مذكرة دفاع",
            "البحث في الموقع",
            "شات مفتوح",
            "لوحة الادمن",
        ],
    )

    if st.sidebar.button("تسجيل الخروج"):
        _log_activity(user["username"], "LOGOUT")
        st.session_state.pop("user_id", None)
        st.rerun()

    if page == "تحليل عقود":
        _contracts_page(users, ai, user)
    elif page == "تحليل قضايا ودفوع":
        _cases_page(users, ai, user)
    elif page == "إنشاء مذكرة دفاع":
        _memo_page(users, ai, user)
    elif page == "البحث في الموقع":
        _search_page(users, law_client, user)
    elif page == "شات مفتوح":
        _chat_page(users, ai, user)
    elif page == "لوحة الادمن":
        _admin_dashboard(users, user)


if __name__ == "__main__":
    main()
