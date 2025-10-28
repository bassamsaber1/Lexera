enum 50105 "CRM Activity Status"
{
    Extensible = true;
    Caption = 'Activity Status';

    value(0; Planned)
    {
        Caption = 'Planned';
    }
    value(1; "In Progress")
    {
        Caption = 'In Progress';
    }
    value(2; Completed)
    {
        Caption = 'Completed';
    }
    value(3; Cancelled)
    {
        Caption = 'Cancelled';
    }
}
