def missing(swag, actual):
    swag_parsed = [x[0] for x in swag]
    needed = []
    for x in actual:
        if x[0] not in swag_parsed:
            print x
            needed.append(x[1].replace(" ", "_"))
    return needed

def make_swag(items, indent):
    return ",\n".join(
        ['{spaces}"{item}": {{\n{spaces}    "type": "string"\n{spaces}}}'.format(
            spaces=indent, item=item) for item in items])

a = """Campaign Owner   Campaign Owner  SSelect the name of the user to whom the campaign is assigned.  Pick list   -
Campaign Name*  Campaign Name*  Specify the name of the campaign.   Text box    Alphanumeric(40)
Type    Type    Select the type of the campaign.    Check box   -
Status  Status  Select the status of the campaign.  Pick List   -
Start Date  Start Date  Specify the date on which the campaign starts.  Date format -
End Date    End Date    Specify the date on which the campaign ends.    Date format -
Expected Revenue    Expected Revenue    Specify the revenue expected after launching the campaign.  Currency    -
Actual Cost  Actual Cost Specify the actual amount spent on the campaign.    Currency    -
Budgeted Cost   Budgeted Cost   Specify the planned amount to be spent on the campaign. Currency    -
Expected Response   Expected Response   Specify the campaign turnout percentage.    Number   
Num sent    Num sent    Specify the number of leads/contacts to whom the campaign details has been sent.    Text box    Integers
Description  Description Specify additional details about the campaign.  Text area   32000 characters"""

act = [
    (x.split("  ")[0].replace(" ","").upper(), x.split("  ")[0])
    for x in a.replace("*", " ").split("\n")
    if x.split("  ")[0] != ""
]

cur = [
    (x.replace("_","").upper(), x)
    for x in b.keys()
]

d = missing(cur, act)
print make_swag(d, " " * 12)
