import tkinter as tk
from tkinter import messagebox, ttk
import requests
from PIL import Image, ImageTk
import webbrowser

class FitnessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fitness and Recipe App")
        self.root.geometry("800x600")
        
        # Define colors
        self.primary_color = "#FF5733"
        self.secondary_color = "#FFC300"
        self.background_color = "#F9EBEA"
        self.button_color = "#FF5733"
        
        # Apply background color to root window
        self.root.configure(background=self.background_color)
        
        # Create a notebook widget to switch between different functionalities
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")
        
        # Add tabs for diet and recipe functionalities
        self.diet_tab = tk.Frame(self.notebook, bg=self.background_color)
        self.recipe_tab = tk.Frame(self.notebook, bg=self.background_color)
        
        self.notebook.add(self.diet_tab, text="Diet Plan")
        self.notebook.add(self.recipe_tab, text="Recipe Recommendation")
        
        # Initialize diet plan and recipe recommendation sections
        self.init_diet_section()
        self.init_recipe_section()
        
    def init_diet_section(self):
        # Diet Plan Section
        label_gender = tk.Label(self.diet_tab, text="Gender:", bg=self.background_color)
        label_gender.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        
        self.gender_var = tk.StringVar()
        self.gender_var.set("Male")
        gender_options = ["Male", "Female"]
        gender_menu = ttk.Combobox(self.diet_tab, textvariable=self.gender_var, values=gender_options, state="readonly")
        gender_menu.grid(row=0, column=1, padx=5, pady=5)
        
        label_weight = tk.Label(self.diet_tab, text="Weight (kg):", bg=self.background_color)
        label_weight.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        
        self.entry_weight = tk.Entry(self.diet_tab)
        self.entry_weight.grid(row=1, column=1, padx=5, pady=5)
        
        label_height = tk.Label(self.diet_tab, text="Height (cm):", bg=self.background_color)
        label_height.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        
        self.entry_height = tk.Entry(self.diet_tab)
        self.entry_height.grid(row=2, column=1, padx=5, pady=5)

        label_age = tk.Label(self.diet_tab, text="Age:", bg=self.background_color)
        label_age.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        
        self.entry_age = tk.Entry(self.diet_tab)
        self.entry_age.grid(row=3, column=1, padx=5, pady=5)

        label_activity_level = tk.Label(self.diet_tab, text="Activity Level:", bg=self.background_color)
        label_activity_level.grid(row=4, column=0, padx=5, pady=5, sticky="e")

        self.activity_level_var = tk.StringVar()
        self.activity_level_var.set("Sedentary")
        activity_level_options = ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"]
        activity_level_menu = ttk.Combobox(self.diet_tab, textvariable=self.activity_level_var, values=activity_level_options, state="readonly")
        activity_level_menu.grid(row=4, column=1, padx=5, pady=5)

        button_calculate_diet = tk.Button(self.diet_tab, text="Calculate Diet Plan", command=self.calculate_diet, bg=self.button_color, fg="white")
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
        label_ingredients = tk.Label(self.recipe_tab, text="Enter Ingredients (comma-separated):", bg=self.background_color)
        label_ingredients.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        
        self.entry_ingredients = tk.Entry(self.recipe_tab)
        self.entry_ingredients.grid(row=0, column=1, padx=5, pady=5)
        
        button_search_recipe = tk.Button(self.recipe_tab, text="Search Recipe", command=self.search_recipe, bg=self.button_color, fg="white")
        button_search_recipe.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        self.recipe_result_frame = tk.Frame(self.recipe_tab, bg=self.background_color)
        self.recipe_result_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        
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
            self.display_recipe_images(data["hits"])
        else:
            messagebox.showinfo("No Recipes Found", "No recipes found with the provided ingredients.")
    
    def display_recipe_images(self, hits):
        # Clear previous results
        for widget in self.recipe_result_frame.winfo_children():
            widget.destroy()
        
        # Display recipe images
        for i, hit in enumerate(hits):
            recipe_image_url = hit["recipe"]["image"]
            recipe_title = hit["recipe"]["label"]
            
            # Fetch image from URL
            response = requests.get(recipe_image_url)
            image_data = response.content
            image = Image.open(io.BytesIO(image_data))
            image = image.resize((150, 150), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
            
            # Create label with recipe image
            image_label = tk.Label(self.recipe_result_frame, image=photo, bg=self.background_color)
            image_label.image = photo
            image_label.grid(row=i//2, column=i%2, padx=5, pady=5)
            image_label.bind("<Button-1>", lambda event, url=hit["recipe"]["url"]: self.open_recipe_url(url))
    
    def open_recipe_url(self, url):
        webbrowser.open(url)

# Create the main window
root = tk.Tk()
app = FitnessApp(root)
root.mainloop()
