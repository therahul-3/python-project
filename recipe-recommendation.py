import tkinter as tk
from tkinter import messagebox, ttk
import requests

class FitnessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fitness and Recipe App")
        self.root.geometry("400x300")
        
        # Create a notebook widget to switch between different functionalities
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")
        
        # Add tabs for diet and recipe functionalities
        self.diet_tab = tk.Frame(self.notebook)
        self.recipe_tab = tk.Frame(self.notebook)
        
        self.notebook.add(self.diet_tab, text="Diet Plan")
        self.notebook.add(self.recipe_tab, text="Recipe Recommendation")
        
        # Initialize diet plan and recipe recommendation sections
        self.init_diet_section()
        self.init_recipe_section()
        
    def init_diet_section(self):
        # Diet Plan Section
        label_gender = tk.Label(self.diet_tab, text="Gender:")
        label_gender.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        
        self.gender_var = tk.StringVar()
        self.gender_var.set("Male")
        gender_options = ["Male", "Female"]
        gender_menu = ttk.Combobox(self.diet_tab, textvariable=self.gender_var, values=gender_options, state="readonly")
        gender_menu.grid(row=0, column=1, padx=5, pady=5)
        
        label_weight = tk.Label(self.diet_tab, text="Weight (kg):")
        label_weight.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        
        self.entry_weight = tk.Entry(self.diet_tab)
        self.entry_weight.grid(row=1, column=1, padx=5, pady=5)
        
        label_height = tk.Label(self.diet_tab, text="Height (cm):")
        label_height.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        
        self.entry_height = tk.Entry(self.diet_tab)
        self.entry_height.grid(row=2, column=1, padx=5, pady=5)

        label_age = tk.Label(self.diet_tab, text="Age:")
        label_age.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        
        self.entry_age = tk.Entry(self.diet_tab)
        self.entry_age.grid(row=3, column=1, padx=5, pady=5)

        label_activity_level = tk.Label(self.diet_tab, text="Activity Level:")
        label_activity_level.grid(row=4, column=0, padx=5, pady=5, sticky="e")

        self.activity_level_var = tk.StringVar()
        self.activity_level_var.set("Sedentary")
        activity_level_options = ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"]
        activity_level_menu = ttk.Combobox(self.diet_tab, textvariable=self.activity_level_var, values=activity_level_options, state="readonly")
        activity_level_menu.grid(row=4, column=1, padx=5, pady=5)

        button_calculate_diet = tk.Button(self.diet_tab, text="Calculate Diet Plan", command=self.calculate_diet)
        button_calculate_diet.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        
    def calculate_diet(self):
        gender = self.gender_var.get()
        weight = float(self.entry_weight.get())
        height = float(self.entry_height.get()) / 100  # Convert height from cm to meters
        age = int(self.entry_age.get())

        # Calculate Basal Metabolic Rate (BMR) based on gender, weight, height, and age
        if gender == "Male":
            bmr = 10 * weight + 6.25 * height * 100 - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height * 100 - 5 * age - 161

        # Adjust BMR based on activity level
        activity_level = self.activity_level_var.get()
        if activity_level == "Sedentary":
            bmr *= 1.2
        elif activity_level == "Lightly Active":
            bmr *= 1.375
        elif activity_level == "Moderately Active":
            bmr *= 1.55
        elif activity_level == "Very Active":
            bmr *= 1.725

        # Calculate total daily calorie intake based on BMR and activity level
        calorie_intake = bmr

        # Display diet plan in a message box
        diet_plan = f"Your daily calorie intake: {calorie_intake:.2f} kcal\n\n"\
                    "Sample Diet Plan:\n"\
                    "- Breakfast: Whole grain cereal with low-fat milk\n"\
                    "- Snack: Greek yogurt with fruits\n"\
                    "- Lunch: Grilled chicken breast with quinoa and steamed vegetables\n"\
                    "- Snack: Protein shake\n"\
                    "- Dinner: Baked salmon with sweet potatoes and broccoli"
        messagebox.showinfo("Diet Plan", diet_plan)
        
    def init_recipe_section(self):
        # Recipe Recommendation Section
        label_ingredients = tk.Label(self.recipe_tab, text="Enter Ingredients (comma-separated):")
        label_ingredients.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        
        self.entry_ingredients = tk.Entry(self.recipe_tab)
        self.entry_ingredients.grid(row=0, column=1, padx=5, pady=5)
        
        button_search_recipe = tk.Button(self.recipe_tab, text="Search Recipe", command=self.search_recipe)
        button_search_recipe.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        self.recipe_result_label = tk.Label(self.recipe_tab, text="")
        self.recipe_result_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        
    def search_recipe(self):
        ingredients = self.entry_ingredients.get()
        if not ingredients:
            messagebox.showwarning("Warning", "Please enter ingredients.")
            return
        
        # Fetch recipe data from Edamam Recipe Search API
        url = f"https://api.edamam.com/search?q={ingredients}&app_id=YOUR_EDAMAM_APP_ID&app_key=YOUR_EDAMAM_API_KEY&to=5"
        # Replace 'YOUR_EDAMAM_APP_ID' and 'YOUR_EDAMAM_API_KEY' with your actual credentials
        response = requests.get(url)
        data = response.json()
        
        # Display recipe results
        if "hits" in data and data["hits"]:
            recipes = [hit["recipe"]["label"] for hit in data["hits"]]
            recipe_list = "\n\n".join([f"{i+1}. {recipe}" for i, recipe in enumerate(recipes)])
            self.recipe_result_label.config(text=recipe_list)
        else:
            self.recipe_result_label.config(text="No recipes found with the provided ingredients.")

# Create the main window
root = tk.Tk()
app = FitnessApp(root)
root.mainloop()
