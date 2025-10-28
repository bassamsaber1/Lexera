enum 50101 "CRM Customer Status"
{
    Extensible = true;
    Caption = 'Customer Status';

    value(0; Prospect)
    {
        Caption = 'Prospect';
    }
    value(1; Lead)
    {
        Caption = 'Lead';
    }
    value(2; Opportunity)
    {
        Caption = 'Opportunity';
    }
    value(3; Customer)
    {
        Caption = 'Customer';
    }
    value(4; Inactive)
    {
        Caption = 'Inactive';
    }
}
