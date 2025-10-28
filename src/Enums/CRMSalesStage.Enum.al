enum 50102 "CRM Sales Stage"
{
    Extensible = true;
    Caption = 'Sales Stage';

    value(0; Qualification)
    {
        Caption = 'Qualification';
    }
    value(1; "Needs Analysis")
    {
        Caption = 'Needs Analysis';
    }
    value(2; Proposal)
    {
        Caption = 'Proposal';
    }
    value(3; Negotiation)
    {
        Caption = 'Negotiation';
    }
    value(4; "Closed Won")
    {
        Caption = 'Closed Won';
    }
    value(5; "Closed Lost")
    {
        Caption = 'Closed Lost';
    }
}
