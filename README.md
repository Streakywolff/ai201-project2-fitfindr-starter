FitFindr is a tool that helps user find clothing and styles it based on their wardrobe. The agent searches a thrift listing database, suggest outfit combinations, and generates a shareable fit card. It uses a planning loop to decide which tools to call next and passes information between tools using session state.

Tool Inventory:
    search_listing(description,size,max_prize)
        purpose:
            Search the listing database for clothing items matching the users request.
        Inputs:
            description(str): clothing description or style
            size(str): desired size
            max_prize:(float)
        Output:
            list[dict]: matching listing dictionaries sorted by relevance
        failure Handling:
            Return an empty list if no matching items are found
    
    suggest_outfit(new_item,wardrobe)
        purpose:
            creates outfit suggestions using the selected listing and the user's wardrobe
        inputs:
            new_item(dict): selected clothing item
            wardrobe(dict): user's wardrobe data
        output:
            str:outfit recommendation
        failure handling:
        if the wardrobe is empty, general styling advice is generated instea.

    create_fit_card(outfit, new_item)
    purpose:
        Generate a shot social-media style caption describing the outfit.
    inputs:
        Outfit(str): outfit recommendation
        new_item(dict): selected clothing item
    output:
        str:sharable fit card
    Failure Handling:
        Returns an error message if the outfit string is empty
    
Planning loop
    Parse the users query
    call search_listing()
    if not listing are found, stop and return an error message
    select the heightest-ranked listing
    pass the selected listing and wardrobe into suggest_outfit()
    pass the outfit suggestion and selected listing into create_fit_card().
    Return the compeleted session
    The agent does not call all tools, it only proceeds when the previous step is successfull

State Management
    The agent stores information inside a session dictionary. The selected item returned from search_listings() is passed into suggest_outfit(). The outfit suggestion returned from suggest_outfit() is passed into create_fit_card().

Error handling

    search_listings
        If no listings match the query, the tool returns an empty list. The agent stops and tells the user to broaden their search or increase their budget.
    suggest_outfit
        If the wardrobe is empty, the tool generates general styling advice instead of failing.

    create_fit_card
        If the outfit string is empty, the tool returns:
        "Unable to create fit card because no outfit suggestion was provided."
Spec Reflection
    The planning document really helped define inputs, output, and any failure that might arise. This made tackling any issues super easy. One implementation issue was the search ranking logic.
AI useage
    I used Chatgpt to help plan and remove some of the manual processes. Additonally chatgpt was heavly useful for debuging and helping to code. I reviewd the code it provided and tested it to see if the outputs where correct.

