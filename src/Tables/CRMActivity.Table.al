table 50102 "CRM Activity"
{
    Caption = 'Activity';
    DataClassification = CustomerContent;

    fields
    {
        field(1; "No."; Code[20])
        {
            Caption = 'No.';
            DataClassification = CustomerContent;
        }
        field(2; Description; Text[100])
        {
            Caption = 'Description';
            DataClassification = CustomerContent;
        }
        field(3; "Activity Type"; Enum "CRM Activity Type")
        {
            Caption = 'Activity Type';
            DataClassification = CustomerContent;
        }
        field(4; "Contact No."; Code[20])
        {
            Caption = 'Contact No.';
            DataClassification = CustomerContent;
            TableRelation = "CRM Contact"."No.";
        }
        field(5; "Contact Name"; Text[100])
        {
            Caption = 'Contact Name';
            FieldClass = FlowField;
            CalcFormula = lookup("CRM Contact".Name where("No." = field("Contact No.")));
            Editable = false;
        }
        field(6; "Opportunity No."; Code[20])
        {
            Caption = 'Opportunity No.';
            DataClassification = CustomerContent;
            TableRelation = "CRM Opportunity"."No.";
        }
        field(7; "Start Date/Time"; DateTime)
        {
            Caption = 'Start Date/Time';
            DataClassification = CustomerContent;
        }
        field(8; "End Date/Time"; DateTime)
        {
            Caption = 'End Date/Time';
            DataClassification = CustomerContent;
        }
        field(9; "Assigned To"; Code[20])
        {
            Caption = 'Assigned To';
            DataClassification = CustomerContent;
        }
        field(10; Status; Enum "CRM Activity Status")
        {
            Caption = 'Status';
            DataClassification = CustomerContent;
        }
        field(11; Priority; Enum "CRM Activity Priority")
        {
            Caption = 'Priority';
            DataClassification = CustomerContent;
        }
        field(12; Notes; Text[250])
        {
            Caption = 'Notes';
            DataClassification = CustomerContent;
        }
    }

    keys
    {
        key(PK; "No.")
        {
            Clustered = true;
        }
        key(Contact; "Contact No.")
        {
        }
        key(Opportunity; "Opportunity No.")
        {
        }
    }
}
