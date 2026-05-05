# importing
import sqlite3
import time


def init_db():
    conn = sqlite3.connect('kitchen.db')
    cursor = conn.cursor()

    # 1. Ingredient List Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ingredient_list (
            item TEXT PRIMARY KEY,
            stock_count INTEGER,
            critical_count INTEGER,
            units TEXT
        )
    ''')

    # 2. Recipe Amounts Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipe_amounts (
            item TEXT PRIMARY KEY,
            required_amount INTEGER,
            units TEXT
        )
    ''')

    # 3. Kitchen Tools Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mutfak_araclari (
            urun TEXT PRIMARY KEY,
            ekstrasi TEXT,
            durum_ana TEXT,
            durum_ekst TEXT
        )
    ''')

    # Table for Service Accompaniments
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS yaninda (
                urun TEXT PRIMARY KEY,
                eldeki_sayi INTEGER,
                birimler TEXT
            )
        ''')

    tools = [
        ('spatula', 'kasik', 'mevcut', 'mevcut'),
        ('tava', 'sahan', 'mevcut', 'mevcut'),
        ('kesme tahtasi', 'none', 'mevcut', 'none'),
        ('kase', 'derin tabak', 'none', 'none')
    ]

    cursor.executemany('INSERT OR IGNORE INTO mutfak_araclari VALUES (?,?,?,?)', tools)

    sides = [
        ('Bread', 5, 'slices'),
        ('Tea', 10, 'cups'),
        ('Cheese', 4, 'slices')
    ]
    cursor.executemany('INSERT OR IGNORE INTO yaninda VALUES (?,?,?)', sides)

    ingredients = [
        ('Tomato', 3, 1, 'piece'),
        ('Pepper', 5, 2, 'piece'),
        ('Egg', 10, 2, 'piece'),  # Increased egg seed for testing
        ('Oil', 10, 1, 'spoon'),
        ('Spices', 10, 1, 'teaspoon'),
        ('Onion', 5, 1, 'piece')
    ]
    cursor.executemany('INSERT OR IGNORE INTO ingredient_list VALUES (?,?,?,?)', ingredients)

    recipe = [
        ('Tomato', 3, 'piece'),
        ('Pepper', 5, 'piece'),
        ('Egg', 2, 'piece'),
        ('Oil', 2, 'spoon'),
        ('Spices', 1, 'teaspoon'),
        ('Onion', 1, 'piece')
    ]
    cursor.executemany('INSERT OR IGNORE INTO recipe_amounts VALUES (?,?,?)', recipe)

    conn.commit()
    conn.close()
    print("Database initialized (and persisted) successfully.")

# side functions
def waste_management(items):
    # Check if the input is a list or just a single string
    if isinstance(items, list):
        for item in items:
            print(f"   [Waste Management] {item} waste has been separated.")
    else:
        print(f"   [Waste Management] {items} waste has been separated.")



def temizle(urun_listesi):
    print("\n--- Cleaning Process Started (Temizle) ---")

    # Are there items left in the list?)
    while urun_listesi:
        current_item = urun_listesi.pop(0)
        print(f"\nProcessing: {current_item['name']}")

        # Ingredient or Kitchen Tool?
        if current_item['type'] == 'mutfak gereci':
            print(f"   [Tool] Washing {current_item['name']} with a soapy sponge.")
            print(f"   [Tool] Rinsing {current_item['name']} with hot water.")

            # Is it dry?
            while True:
                is_dry = input(f"   Is {current_item['name']} dry? (yes/no): ").lower().strip()
                if is_dry == 'yes':
                    break
                else:
                    print("   Waiting for it to dry...")
                    time.sleep(1)  # Rinsing/Waiting simulation

        elif current_item['type'] == 'malzeme':
            print(f"   [Ingredient] Rinsing {current_item['name']} under cold water.")

            # Is it dry?
            while True:
                print(f"   [Ingredient] Drying {current_item['name']}...")
                is_dry = input(f"   Is {current_item['name']} dry? (yes/no): ").lower().strip()
                if is_dry == 'yes':
                    break
                else:
                    print("   Continuing to dry/drain...")

    print("\n--- Cleaning Complete. No items left in list. (End) ---")


def check_multiple_ingredients(conn, item_list):

    print(f"--- Inventory Check Started for {len(item_list)} items ---")


    cursor = conn.cursor()

    for item_name in item_list:
        cursor.execute('''
            SELECT stock_count, critical_count FROM ingredient_list 
            WHERE item = ?
        ''', (item_name,))
        result = cursor.fetchone()

        if not result:
            print(f"  [!] {item_name} not found in database. Skipping.")
            continue

        stock_count, critical_count = result

        if stock_count < critical_count:

            # 1. Calculate the required amount
            deficit = stock_count - critical_count
            print(f"  [-] {item_name} is LOW ({stock_count}/{critical_count}). Deficit: {abs(deficit)}")


            # 3. UPDATE DB: stock_count + (3 * critical_count)
            new_stock = stock_count + (3 * critical_count)
            cursor.execute('''
                UPDATE ingredient_list 
                SET stock_count = ? 
                WHERE item = ?
            ''', (new_stock, item_name))
        else:
            print(f"  [+] {item_name} stock is sufficient.")

    # Finalize all updates at once
    conn.commit()
    print("--- Inventory Check Complete (End) ---")



def buy_tool(tool_name):

    print(f"   [PURCHASE] {tool_name} is being ordered.")


def check_multiple_tools(conn,tool_list):
    print(f"--- Kitchen Tools Check Started for {len(tool_list)} items ---")


    cursor = conn.cursor()

    for tool_name in tool_list:
        cursor.execute('''
            SELECT urun, ekstrasi, durum_ana, durum_ekst 
            FROM mutfak_araclari 
            WHERE urun = ?
        ''', (tool_name,))
        result = cursor.fetchone()

        if not result:
            print(f"   [!] {tool_name} not found in tools database. Skipping.")
            continue

        item, extra, status_main, status_extra = result

        # Is the main tool available?
        if status_main == 'mevcut':
            # Evet (Yes) -> End
            print(f"   [+] {item} is available.")
        else:
            # Decision 2: Is the alternative available?
            if status_extra == 'mevcut':
                # Yes -> End
                print(f"   [+] {item} missing, but alternative ({extra}) is available.")
            else:
                # No
                print(f"   [-] Neither {item} nor {extra} are available!")

                #Buy the tool
                buy_tool(item)

                # UPDATE DB
                cursor.execute('''
                    UPDATE mutfak_araclari 
                    SET durum_ana = 'mevcut' 
                    WHERE urun = ?
                ''', (item,))
                print(f"   [DB Update] {item} status set to 'mevcut'.")

    conn.commit()
    print("--- Kitchen Tools Check Complete (End) ---")


def update_final_stock(conn, item_list):
    cursor = conn.cursor()
    for item in item_list:
        cursor.execute('''
            UPDATE ingredient_list
            SET stock_count = stock_count - (
                SELECT required_amount 
                FROM recipe_amounts 
                WHERE recipe_amounts.item = ingredient_list.item
            )
            WHERE item = ? 
              AND EXISTS (SELECT 1 FROM recipe_amounts WHERE item = ?)
        ''', (item, item))
    conn.commit()
    print("   [DB Update] Actual recipe amounts deducted from stock.")


def is_inventory_sufficient(conn, item_list):
    cursor = conn.cursor()
    insufficient_items = []

    for item_name in item_list:
        cursor.execute('''
            SELECT il.item, il.stock_count, ra.required_amount 
            FROM ingredient_list il
            JOIN recipe_amounts ra ON il.item = ra.item
            WHERE il.item = ?
        ''', (item_name,))

        result = cursor.fetchone()
        if result:
            name, stock, required = result
            if stock < required:
                insufficient_items.append(f"{name} (Need {required}, Have {stock})")
        else:
            insufficient_items.append(f"{item_name} (Missing from Database)")

    return insufficient_items


def preperation(conn):
    print("\n--- Starting Preparation Process (Hazirlik Sureci) ---")
    ingredients_to_check = ["Tomato", "Pepper", "Egg", "Onion"]

    # STEP 1: Tools Check (Standard)
    check_multiple_tools(conn, ["spatula", "tava", "kesme tahtasi", "kase"])

    # STEP 2: Automatic Restock (The "Shopping" phase)
    # This MUST come before the sufficiency check
    check_multiple_ingredients(conn, ingredients_to_check)

    # STEP 3: Sufficiency Check (The "Do I have enough for the recipe?" phase)
    missing = is_inventory_sufficient(conn, ingredients_to_check)

    if missing:
        print("\n CANNOT START COOKING: Insufficient Ingredients!")
        for m in missing:
            print(f"   - {m}")
        print("Please check your database seeding values.")
        return False

    # STEP 4: Physical Prep (Peeling, Dicing, Cracking)
    print("[Pepper] Cutting 1cm from top, slicing length-wise, and dicing...")
    waste_management(["seeds", "white membranes"])

    has_skin = input("Is the tomato peelable/has skin? (yes/no): ").lower().strip()
    if has_skin == "yes":
        print("[Tomato] Cutting head and dicing into 1x1.5cm cubes.")
        waste_management("stems/trash")
    else:
        print("[Tomato] Scoring with an X and peeling gently.")
        waste_management("peels")

    needs_onion = input("Do you want to include onions? (yes/no): ").lower().strip()
    if needs_onion == "yes":
        print("[Onion] Peeling, slicing half-moons, and dicing cubes.")
        waste_management("onion skins")

    print("[Egg] Cracking eggs one by one into a small bowl.")
    while True:
        shell_in = input("Did a piece of shell fall into the bowl? (yes/no): ").lower().strip()
        if shell_in == "yes":
            print("   Action: Removing the shell with a fork...")
        else:
            break
    waste_management("egg shells")

    print("--- Preparation Complete (End) ---")
    return True

def cooking(conn):
    print("\n--- Starting Cooking Process (Pisirme Sureci) ---")

    print("Gathering materials: Spatula, Tomato, Pepper, Onion, Salt, Butter/Oil...")
    print("Gathering tools: Pan, Stove, Spatula, Fork...")
    print("Setting pan on the stove over medium heat.")

    # 1. Oil Selection
    oil_choice = input("Choose oil type - Olive Oil or Butter? (olive/butter): ").lower().strip()
    if oil_choice == "olive":
        print("Adding olive oil and a small piece of butter to the pan.")
    else:
        print("Adding 2-3 tablespoons of butter to the pan.")

    # 2. Heat Check
    while True:
        ready = input("Is the oil hot enough? (yes/no): ").lower().strip()
        if ready == "yes":
            break
        else:
            print("Waiting 20 seconds for the oil to heat...")
            time.sleep(1)  # Simulation

    # 3. Onion Cooking
    has_onion = input("Are you using onions? (yes/no): ").lower().strip()
    if has_onion == "yes":
        print("Adding onions to the pan. Sautéing for 2 minutes.")
        while True:
            pink = input("Are the onions translucent/pink? (yes/no): ").lower().strip()
            if pink == "yes":
                break
            else:
                print("Cooking for 1 more minute...")

    # 4. Pepper Cooking
    print("Adding peppers to the pan.")
    while True:
        print("Stirring peppers and waiting 30 seconds...")
        soft = input("Are the peppers softened and edges slightly browned? (yes/no): ").lower().strip()
        if soft == "yes":
            break

    # 5. Tomato Cooking
    print("Adding diced tomatoes to the pan. Adding salt and spices.")
    print("Cooking for 5 minutes...")
    while True:
        homogenized = input("Has it reached a sauce-like, homogenized consistency? (yes/no): ").lower().strip()
        if homogenized == "yes":
            break
        else:
            print("Cooking for 1 more minute...")

    # 6. Egg Cooking
    print("Pouring the cracked eggs from the bowl into the pan.")
    print("Mixing with the tomato base and cooking for 2 minutes over low heat.")

    while True:
        perfect = input("Has it reached the desired consistency? (yes/no): ").lower().strip()
        if perfect == "yes":
            print("Turning off the stove.")
            update_final_stock(conn, ["Tomato", "Pepper", "Egg", "Onion"])
            break
        else:
            print("Taking it off the heat immediately so it doesn't overcook.")
            update_final_stock(conn, ["Tomato", "Pepper", "Egg", "Onion"])
            break

    print("Turning off the stove.")

    # 8. Clean up
    dirty_items = [
        {'name': 'Tava', 'type': 'mutfak gereci'},
        {'name': 'Spatula', 'type': 'mutfak gereci'}
    ]
    temizle(dirty_items)

    print("--- Cooking Process Complete (End) ---")


def feedback_process(conn, user_name):
    print(f"\n--- Feedback System for {user_name} ---")

    questions = [
        "1. Taste Score (1-10): ",
        "2. Salt Level (Low/Normal/High): ",
        "3. Cooking Consistency (Soggy/Dry): ",
        "4. Visual Appeal Score (1-10): ",
        "5. Freshness of Ingredients (Yes/No): ",
        "6. Recommendation Likelihood (Yes/No): ",
        "7. New Requests (Extra cheese, onion, etc.): "
    ]

    responses = {}

    cursor = conn.cursor()

    for i, q in enumerate(questions, 1):
        answer = input(q)
        responses[f"q{i}"] = answer

        # Is there a response?
        # positive -> save to 'feedback' table; negative -> save to 'errors'
        if answer.strip():
            # Simulated DB Table: feedback (username, question_id, response)
            cursor.execute("CREATE TABLE IF NOT EXISTS feedback (user TEXT, q_id TEXT, ans TEXT)")
            cursor.execute("INSERT INTO feedback VALUES (?, ?, ?)", (user_name, f"q{i}", answer))
        else:
            # Simulated DB Table: error_logs
            cursor.execute("CREATE TABLE IF NOT EXISTS error_logs (user TEXT, q_id TEXT, status TEXT)")
            cursor.execute("INSERT INTO error_logs VALUES (?, ?, ?)", (user_name, f"q{i}", "no_response"))

    conn.commit()
    print("Feedback successfully saved to database. Thank you!")


def serve(conn):
    print("\n--- Starting Service (Servis) ---")

    # 1. Menemen Preparation and Plate
    print("Plating the Menemen...")

    # 2. Accompaniments

    cursor = conn.cursor()

    add_sides = input("Would you like side items (Bread, Tea, Cheese)? (yes/no): ").lower().strip()
    if add_sides == "yes":
        cursor.execute("SELECT urun, eldeki_sayi, birimler FROM yaninda")
        sides = cursor.fetchall()
        for side, count, unit in sides:
            if count > 0:
                print(f"   [Adding Side] {side} ({count} {unit} available)")
                # Update DB: stock - 1
                cursor.execute("UPDATE yaninda SET eldeki_sayi = eldeki_sayi - 1 WHERE urun = ?", (side,))

    conn.commit()

    # 3. User Feedback Trigger
    user_name = input("Enter your name for the feedback session: ")
    feedback_process(conn, user_name)

    # 4. Final Cleaning
    print("\nClearing the table...")
    items_to_clean = ["plate", "fork", "knife", "pan", "glass"]
    temizle([{'name': item, 'type': 'mutfak gereci'} for item in items_to_clean])

    print("--- Service Process Complete (End) ---")


if __name__ == "__main__":
    init_db()
    main_conn = sqlite3.connect('kitchen.db')

    try:
        while True:
            hungry = input("\nAre you hungry? (Yes/No) [Press 'q' to quit]: ").strip().lower()
            if hungry == "q": break

            if hungry == "yes":
                # Only cook if preparation was successful
                if preperation(main_conn):
                    cooking(main_conn)
                    serve(main_conn)
                    print("\nSimulation cycle complete!")
                else:
                    print("\nCycle aborted due to missing supplies.")
    finally:
        main_conn.close()