page 50103 "CRM Opportunity List"
{
    Caption = 'Opportunities';
    PageType = List;
    SourceTable = "CRM Opportunity";
    UsageCategory = Lists;
    ApplicationArea = All;
    CardPageId = "CRM Opportunity Card";

    layout
    {
        area(Content)
        {
            repeater(Group)
            {
                field("No."; Rec."No.")
                {
                    ApplicationArea = All;
                    ToolTip = 'Specifies the opportunity number.';
                }
                field(Description; Rec.Description)
                {
                    ApplicationArea = All;
                    ToolTip = 'Specifies the opportunity description.';
                }
                field("Contact No."; Rec."Contact No.")
                {
                    ApplicationArea = All;
                    ToolTip = 'Specifies the contact number.';
                }
                field("Contact Name"; Rec."Contact Name")
                {
                    ApplicationArea = All;
                    ToolTip = 'Specifies the contact name.';
                }
                field("Sales Stage"; Rec."Sales Stage")
                {
                    ApplicationArea = All;
                    ToolTip = 'Specifies the current sales stage.';
                }
                field(Status; Rec.Status)
                {
                    ApplicationArea = All;
                    ToolTip = 'Specifies the opportunity status.';
                }
                field("Estimated Value"; Rec."Estimated Value")
                {
                    ApplicationArea = All;
                    ToolTip = 'Specifies the estimated value.';
                }
                field("Probability %"; Rec."Probability %")
                {
                    ApplicationArea = All;
                    ToolTip = 'Specifies the probability percentage.';
                }
                field("Expected Close Date"; Rec."Expected Close Date")
                {
                    ApplicationArea = All;
                    ToolTip = 'Specifies the expected close date.';
                }
                field("Salesperson Code"; Rec."Salesperson Code")
                {
                    ApplicationArea = All;
                    ToolTip = 'Specifies the salesperson code.';
                }
            }
        }
    }
}
