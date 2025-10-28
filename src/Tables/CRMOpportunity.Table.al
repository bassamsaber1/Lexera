table 50101 "CRM Opportunity"
{
    Caption = 'Opportunity';
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
        field(3; "Contact No."; Code[20])
        {
            Caption = 'Contact No.';
            DataClassification = CustomerContent;
            TableRelation = "CRM Contact"."No.";
        }
        field(4; "Contact Name"; Text[100])
        {
            Caption = 'Contact Name';
            FieldClass = FlowField;
            CalcFormula = lookup("CRM Contact".Name where("No." = field("Contact No.")));
            Editable = false;
        }
        field(5; "Sales Stage"; Enum "CRM Sales Stage")
        {
            Caption = 'Sales Stage';
            DataClassification = CustomerContent;
        }
        field(6; "Estimated Value"; Decimal)
        {
            Caption = 'Estimated Value';
            DataClassification = CustomerContent;
            AutoFormatType = 1;
        }
        field(7; "Probability %"; Decimal)
        {
            Caption = 'Probability %';
            DataClassification = CustomerContent;
            MinValue = 0;
            MaxValue = 100;
        }
        field(8; "Expected Close Date"; Date)
        {
            Caption = 'Expected Close Date';
            DataClassification = CustomerContent;
        }
        field(9; "Salesperson Code"; Code[20])
        {
            Caption = 'Salesperson Code';
            DataClassification = CustomerContent;
        }
        field(10; Status; Enum "CRM Opportunity Status")
        {
            Caption = 'Status';
            DataClassification = CustomerContent;
        }
        field(11; "Creation Date"; Date)
        {
            Caption = 'Creation Date';
            DataClassification = CustomerContent;
        }
        field(12; "Closed Date"; Date)
        {
            Caption = 'Closed Date';
            DataClassification = CustomerContent;
        }
        field(13; Notes; Text[250])
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
    }
}
