
class RecipesSite:
    next_id = 0
    all_recipes = {} # maps recipe ID to recipe
    admins = {} # maps admin username to admin
    users = {} # maps user username to user
    current_user = None
    current_user_admin = False

    def print_all_recipe_options():
        if len(RecipesSite.all_recipes) == 0:
            print("\nNo recipes yet to show...")
            return
        print("\nAll Recipes:")
        count = 1
        for _, recipe in RecipesSite.all_recipes.items():
            print(f"[{str(count)}] {recipe.name}")
            count += 1

    def run_program():
        RecipesSite.read_from_file()
        RecipesSite.debug_print_data()
        while True:
            if not RecipesSite.current_user:
                # prompt login
                RecipesSite.prompt_home()
            elif RecipesSite.current_user_admin:
                # prompt admin
                RecipesSite.current_user.prompt_admin()
            else:
                # promt user
                RecipesSite.current_user.prompt_user()

    def login_admin():
        prompt_login = True
        while (prompt_login):
            username = input("\nPlease enter your admin username: ")
            password = input("Please enter your password: ")

            if username not in RecipesSite.admins or RecipesSite.admins[username].password != password:
                option = int(input("\nUsername or password is incorrect. \n[1] Try logging in again \n[2] Return home\n"))
                match option:
                    case 1:
                        continue
                    case 2:
                        return
                    case _:
                        print("Not a valid option... please try again")
                        continue
            else:
                prompt_login = False
                RecipesSite.current_user_admin = True
                RecipesSite.current_user = RecipesSite.admins[username]

    def login_user():
        prompt_login = True
        while (prompt_login):
            username = input("\nPlease enter your user username: ")
            password = input("Please enter your password: ")

            if username not in RecipesSite.users or RecipesSite.users[username].password != password:
                option = int(input("\nUsername or password is incorrect.\n[1] Try logging in again \n[2] Return home\n"))
                match option:
                    case 1:
                        continue
                    case 2:
                        return
                    case _:
                        print("Not a valid option... please try again")
                        continue
            else:
                prompt_login = False
                RecipesSite.current_user_admin = False
                RecipesSite.current_user = RecipesSite.users[username]

    def find_next_id():
        while(True):
            if RecipesSite.next_id in RecipesSite.all_recipes:
                RecipesSite.next_id += 1
            else:
                return RecipesSite.next_id
        
    def create_new_acc():
        create_acc = True
        while(create_acc):
            option = int(input("\n[1] Create a new admin account\n[2] Create a new user account\n[3] Return home\n"))
            match option:
                case 1:
                    username = input("\nPlease enter a username: ")
                    if username in RecipesSite.admins:
                        print("Sorry, username is already taken. Please try again.")
                        continue
                    password = input("Please enter a password: ")
                    RecipesSite.admins[username] = Admin(username, password)
                    RecipesSite.current_user = RecipesSite.admins[username]
                    RecipesSite.current_user_admin = True
                    print("\nAccount successfully created and logged in.")
                    RecipesSite.write_to_file()
                    create_acc = False
                case 2:
                    username = input("\nPlease enter a username: ")
                    if username in RecipesSite.users:
                        print("Sorry, username is already taken. Please try again.")
                        continue
                    password = input("Please enter a password: ")
                    RecipesSite.users[username] = User(username, password)
                    RecipesSite.current_user = RecipesSite.users[username]
                    RecipesSite.current_user_admin = False
                    print("\nAccount successfully created and logged in.")
                    RecipesSite.write_to_file()
                    create_acc = False
                case 3:
                    return
                case _:
                    print("Not a valid option... please try again")
                    continue

    def prompt_home():
        print("\nWelcome! Please type 1-3 to login or create a new account.")
        print("[1] Login as admin")
        print("[2] Login as user")
        print("[3] Create a new admin/user account")

        option = int(input())
        match option:
            case 1:
                RecipesSite.login_admin()
            case 2:
                RecipesSite.login_user()
            case 3:
                RecipesSite.create_new_acc()
            case _:
                print("Not a valid option... please try again")

    def write_to_file():
        # write users
        f = open("users.txt", "w")
        for _, user in RecipesSite.users.items():
            f.write(f"{user.username},{user.password}\n")
        f.close()

        # write admins
        f = open("admins.txt", "w")
        for _, admin in RecipesSite.admins.items():
            line = f"{admin.username},{admin.password}"
            for recipe_id in admin.recipes:
                line += f",{recipe_id}"
            f.write(line + "\n")
        f.close()

        # write recipes
        f = open("recipes.txt", "w")
        for _, recipe in RecipesSite.all_recipes.items():
            line = f"{recipe.id},{recipe.name},{recipe.author}"
            for ingredient in recipe.ingredients:
                line += f",{ingredient.name},{ingredient.price},{ingredient.quantity},{ingredient.unit}"
            f.write(line + "\n")
        f.close()

    def read_from_file():
        # read users
        f = open("users.txt", "r")
        for line in f:
            terms = line.rstrip().split(',')
            RecipesSite.users[terms[0]] = User(terms[0], terms[1])
        f.close()

        # read admins
        f = open("admins.txt", "r")
        for line in f:
            terms = line.rstrip().split(',')
            ids = (int(x) for x in terms[2:])
            RecipesSite.admins[terms[0]] = Admin(terms[0], terms[1], list(ids))
        f.close()

        # read recipes
        f = open("recipes.txt", "r")
        for line in f:
            terms = line.rstrip().split(',')
            info = terms[:3]
            ingredients_list = terms[3:]
            ingredients = []
            for name, price, quantity, unit in zip(*[iter(ingredients_list)]*4):
                ingredients.append(Ingredient(name, float(price), float(quantity), unit))
            RecipesSite.all_recipes[int(info[0])] = Recipe(info[1], info[2], ingredients, int(info[0]))
        f.close()
        
    def debug_print_data():
        print(RecipesSite.users)
        print(RecipesSite.admins)
        print(RecipesSite.all_recipes)

class Ingredient:
    def __init__(self, name, price: float, quantity: float, unit):
        self.name = name
        self.price = float(price)
        self.quantity = float(quantity)
        self.unit = unit

    def print_scaled_ingredient(self, scale: float):
        if self.unit == 'None' or self.unit == 'none':
            print(f"{str(self.quantity * scale)} {self.name} - ${str(self.price * scale)}")
        else:
            print(f"{str(self.quantity * scale)} {self.unit} {self.name} - ${str(self.price * scale)}")

    def __str__(self):
        if self.unit == 'None' or self.unit == 'none':
            return f"{str(self.quantity)} {self.name} - ${str(self.price)}"
        return f"{str(self.quantity)} {self.unit} {self.name} - ${str(self.price)}"

class Recipe:
    def __init__(self, name, author, ingredients: list, id=None):
        self.name = name
        self.id = id if id else RecipesSite.find_next_id()
        self.author = author
        self.ingredients = ingredients
        self.total_cost = sum(x.price for x in ingredients)

    def print_scaled_recipe(self, scale):
        print(f"\nRecipe for {self.name}\nAuthor: {self.author}")
        print(f"\nNote: this recipe is {scale}x the original.\n")
        for ingredient in self.ingredients:
            ingredient.print_scaled_ingredient(scale)

    def recipe_as_list_str(self):
        output = f"{self.name}:"
        for ingredient in self.ingredients:
            output += f"\n  {ingredient.__str__()}"
        return output

    def __str__(self):
        output = f"Recipe for {self.name}\nAuthor: {self.author}"
        for ingredient in self.ingredients:
            output += f"\n{ingredient.__str__()}"
        return output

class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.recipes = [] # list of recipe nums

    def __init__(self, username, password, recipe_ids: list):
        self.username = username
        self.password = password
        self.recipes = recipe_ids

    def add_recipe(self, name, ingredients: list):
        new_recipe = Recipe(name, self.username, ingredients)
        self.recipes.append(new_recipe.id)
        RecipesSite.all_recipes[new_recipe.id] = new_recipe
        return new_recipe
    
    def remove_recipe(self, recipe_num: int):
        recipe_to_be_removed_id = self.recipes[recipe_num]
        print("\n" + RecipesSite.all_recipes[recipe_to_be_removed_id] + " has been removed.")
        RecipesSite.all_recipes.pop(recipe_to_be_removed_id)
        del self.recipes[recipe_num]

    def print_recipes(self):
        if len(self.recipes) == 0:
            print("\nYou haven't created any recipes yet...")
            return
        print(f"\n{self.username}'s Recipes:")
        count = 1
        for recipe_id in self.recipes:
            print(f"[{str(count)}] {RecipesSite.all_recipes[recipe_id].recipe_as_list_str()}")
            count += 1

    def prompt_admin(self):
        print(f"\nWelcome {self.username}! Please select what you would like to do.")
        print("[1] View all my recipes")
        print("[2] Add new recipe")
        print("[3] Remove recipe")
        print("[4] Log out")

        option = int(input())
        match option:
            case 1:
                self.print_recipes()
            case 2:
                recipe = self.prompt_add_recipe()
                print("\nHere is your newly added recipe:")
                print(recipe)
                RecipesSite.write_to_file()
            case 3:
                if (not self.recipes):
                    print("\nYou don't have any recipes yet...")
                    return
                self.print_recipes()
                num = int(input("\nPlease select the number of the recipe you would like to remove.\n"))
                if num > len(self.recipes):
                    print("Not a valid option... please try again")
                else:
                    self.remove_recipe(num-1)
                    RecipesSite.write_to_file()
            case 4:
                RecipesSite.current_user = None
                print(f"\nGoodbye, {self.username}!")
            case _:
                print("Not a valid option... please try again")

    def prompt_add_recipe(self):
        recipe_name = input("\nPlease enter the name of your recipe: ")
        ingredients = []

        more_ingredients = True
        while (more_ingredients):
            name = input("Ingredient name: ")
            price = input("Price: ")
            quantity = input("Quantity: ")
            unit = input("Unit (Enter 'None' if unspecified): ")
            ingredients.append(Ingredient(name, price, quantity, unit))
            more_ingredients = int(input("\nDo you have any other ingredients to add? \n[1] Enter more ingredients \n[2] I'm done with the recipe!\n")) == 1
        new_recipe = self.add_recipe(recipe_name, ingredients)
        return new_recipe

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def select_recipe(self):
        print("\nPlease select a recipe by typing the number.")
        RecipesSite.print_all_recipe_options()
        recipe_num = int(input())
        return recipe_num

    def print_ingredients_calculate_amount(self, recipe_id: int, scale: float):
        recipe = RecipesSite.all_recipes[recipe_id]
        print(f"To make {recipe.name}, you will need the following ingredients:")
        recipe.print_scaled_recipe(scale)
        print(f"\nThe total cost of the recipe is {recipe.total_cost}")
        return recipe.total_cost

    def user_process(self):
        recipe_num = self.select_recipe()
        recipe = RecipesSite.all_recipes[recipe_num]
        scale = float(input("How much would you like to scale your recipe by? Please enter a number."))
        print(self.print_ingredients_calculate_amount(recipe.id), scale)

    def prompt_user(self):
        print(f"\nWelcome {self.username}! Please select what you would like to do.")
        print("[1] View all recipe options")
        print("[2] View a recipe in detail")
        print("[3] Scale a recipe")
        print("[4] Log out")

        option = int(input())
        match option:
            case 1:
                RecipesSite.print_all_recipe_options()
            case 2:
                recipe_selected_idx = self.select_recipe()
                print("\nHere is the recipe:")
                print(list(RecipesSite.all_recipes.items())[recipe_selected_idx-1][1])
            # case 3:
            #     # TODO
            case 3:
                RecipesSite.current_user = None
                print(f"\nGoodbye, {self.username}!")
            case _:
                print("Not a valid option... please try again")

RecipesSite.run_program()

# OTHER TODO:# 
# scale recipe
# create/delete account
# error handling
# reorg functions