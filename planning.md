# FitFindr — planning.md

> Complete this document before writing any implementation code.
> Your spec and agent diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Your planning.md will be reviewed as part of your submission.
> Update it before starting any stretch features.

---

## Tools

List every tool your agent will use. For each tool, fill in all four fields.
You must have at least 3 tools. The three required tools are listed — add any additional tools below them.

### Tool 1: search_listings

**What it does:**
searches available clothinglist based on the users requested items, size, and budget. it returns items based on what they can afford

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `description` (str): The type of style or clothing the user is searching for, such as "vintage graphic tee" or "black cargo pants"
- `size` (str): The users clothing size
- `max_price` (float): the heighest price the user is willing to pay

**What it returns:**
<!-- Describe the return value — what fields does a result contain? -->
A list of matching listings

**What happens if it fails or returns nothing:**
<!-- What should the agent do if no listings match? -->
The agent should tell the user no exact matches were found. Then it should loosen the search by increasing the budget, removing a style keyword, or suggesting a similar item

---

### Tool 2: suggest_outfit

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->
Suggest an outfit using the new item and pieces from the users wardrobe. it tries to match colors, style tags, and clothing categories
**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `new_item` (dict): the clothing listing selected from searching_listing.
- `wardrobe` (dict): the user's saved wardrobe, including tops, bottoms, shoes, and etc

**What it returns:**
<!-- Describe the return value -->
an outfit dictionary

**What happens if it fails or returns nothing:**
<!-- What should the agent do if the wardrobe is empty or no outfit can be suggested? -->
If the wardrobe is empty, the agent should still style the item using general suggestions. If no matching wardrobe pieces exist, it should explain what type of item the user could add to make the outfit work.

---

### Tool 3: create_fit_card

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->
Creates a clean final "fit card" that summarizes the item, outfit, price, and styling advice for the user

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `outfit` (...): The outfit returned from suggest_outfit, including the new item and matching wardrobes pieces

**What it returns:**
<!-- Describe the return value -->
a formated fit card

**What happens if it fails or returns nothing:**
<!-- What should the agent do if the outfit data is incomplete? -->
If outfit data is incomplete, the agent should create a partial fit card using the available information and clearly state what information is missing.

---

### Additional Tools (if any)

<!-- Copy the block above for any tools beyond the required three -->

---

## Planning Loop

**How does your agent decide which tool to call next?**
<!-- Describe the logic your planning loop uses. What does it look at? What conditions change its behavior? How does it know when it's done? -->
The agent first should read the user's request and extract the items descriptions. if the user is searching for a item, the agent should call search_listing first. If listings are returned, the agent uses filter_by_style to rank the best options. then the agent should picked the strongest listingand passes it to suggest_outfit along with the user's wardrobe. After an outfit is created, the agent calls create_fit_card to generate the final response. The agent knows its done, when one item is selected, styled with the users wardrobe. If no listings are found, the loop ends with a helpful fallback suggestion
---

## State Management

**How does information from one tool get passed to the next?**
<!-- Describe how your agent stores and accesses state within a session. What data is tracked? How is it passed between tool calls? -->
The agent stores session state in a dictionary during the interaction. Each tool reads from and updates this shared session state

---

## Error Handling

For each tool, describe the specific failure mode you're handling and what the agent does in response.

| Tool | Failure mode | Agent response |
|------|-------------|----------------|
| search_listings | No results match the query |tells the user, then broadens the search |
| suggest_outfit | Wardrobe is empty | suggest a general outfit using common clothes|
| create_fit_card | Outfit input is missing or incomplete | creates a partial fit card and clearly explains outfits are missing|

---

## Architecture

<!-- Draw a diagram of your agent showing how the components connect:
     User input → Planning Loop → Tools (search_listings, suggest_outfit, create_fit_card)
                                                                          ↕
                                                                          
                                                                   State / Session
     Show what triggers each tool, how state flows between them, and where error paths branch off.
     ASCII art, a Mermaid diagram (https://mermaid.js.org/syntax/flowchart.html), or an embedded
     sketch are all fine. You'll share this diagram with an AI tool when asking it to implement
     the planning loop and each individual tool. -->

---

## AI Tool Plan

<!-- For each part of the implementation below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, your agent diagram)
     - What you expect it to produce
     - How you'll verify the output matches your spec before moving on

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Tool 1 spec (inputs, return value, failure mode) and ask it to implement
     search_listings() using load_listings() from the data loader — then test it against 3 queries
     before trusting it" is a plan. -->

**Milestone 3 — Individual tool implementations:**
I will use ChatGPT to implement each tool and help debug an errors
**Milestone 4 — Planning loop and state management:**
Chatgpt might be helpful with implementing the loop

---

## A Complete Interaction (Step by Step)

Write out what a full user interaction looks like from start to finish — tool call by tool call. Use a specific example query.

**Example user query:** "I'm looking for a vintage graphic tee under $30. I mostly wear baggy jeans and chunky sneakers. What's out there and how would I style it?"

**Step 1:**
<!-- What does the agent do first? Which tool is called? With what input? -->
The agent should extract useful inoforatiom such as description, size, max_price, etc
**Step 2:**
<!-- What happens next? What was returned from step 1? What tool is called now? -->
search_listing returns several matching graphic tees under 30
**Step 3:**
<!-- Continue until the full interaction is complete -->
suggest outfits that matches the tee
**Final output to user:**
<!-- What does the user actually see at the end? -->
FitFindr found a faded oversized vintage band tee for $24 in size medium.