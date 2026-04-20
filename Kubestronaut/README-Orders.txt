# To Create the associated Spreadsheet for that oder/country
python CreateGroupedShippingTab.py "Canada" "Volunteer Name" "volunteer@example.com"
Or
python CreateGroupedShippingTab.py "Canada" "Volunteer Name" "volunteer@example.com" --to-be-confirmed

# To generate the cart and send the verification email
python GenerateShopifyCartFromSpreadsheet.py "https://docs.google.com/spreadsheets/d/XXXXX"

# To Ack the send swags in the Information Gathering Spreadsheet
python AckKubestronautAndGKSwagShipped.py "https://docs.google.com/spreadsheets/d/XXXXX" ORDER-TAG
