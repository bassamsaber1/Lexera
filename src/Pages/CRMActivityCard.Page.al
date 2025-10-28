page 50104 "CRM Activity Card"
{
    Caption = 'Activity Card';
    PageType = Card;
    SourceTable = "CRM Activity";
    UsageCategory = None;

    layout
    {
        area(Content)
        {
            group(General)
            {
                Caption = 'General';
                field("No."; Rec."No.")
                {
                    ApplicationArea = All;
                    ToolTip = 'Specifies the activity number.';
                }
                field(Description; Rec.Description)
                {
                    ApplicationArea = All;
                    ToolTip = 'Specifies the activity description.';
                }
                field("Activity Type"; Rec."Activity Type")
                {
                    ApplicationArea = All;
                    ToolTip = 'Specifies the activity type.';
                }
                field(Status; Rec.Status)
                {
                    ApplicationArea = All;
                    ToolTip = 'Specifies the activity status.';
                }
                field(Priority; Rec.Priority)
                {
                    ApplicationArea = All;
                    ToolTip = 'Specifies the priority.';
                }
                field(Completed; Rec.Completed)
                {
                    ApplicationArea = All;
                    ToolTip = 'Specifies if the activity is completed.';
                }
            }
            group(Related)
            {
                Caption = 'Related To';
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
                field("Opportunity No."; Rec."Opportunity No.")
                {
                    ApplicationArea = All;
                    ToolTip = 'Specifies the opportunity number.';
                }
            }
            group(Schedule)
            {
                Caption = 'Schedule';
                field("Start Date/Time"; Rec."Start Date/Time")
                {
                    ApplicationArea = All;
                    ToolTip = 'Specifies the start date and time.';
                }
                field("End Date/Time"; Rec."End Date/Time")
                {
                    ApplicationArea = All;
                    ToolTip = 'Specifies the end date and time.';
                }
                field("Assigned To"; Rec."Assigned To")
                {
                    ApplicationArea = All;
                    ToolTip = 'Specifies who the activity is assigned to.';
                }
            }
            group(AdditionalInfo)
            {
                Caption = 'Additional Information';
                field(Notes; Rec.Notes)
                {
                    ApplicationArea = All;
                    MultiLine = true;
                    ToolTip = 'Specifies notes about the activity.';
                }
            }
        }
    }
}
