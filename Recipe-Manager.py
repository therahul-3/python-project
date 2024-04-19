# final project recipe manager modify it
import tkinter as tk
from tkinter import messagebox

class Recipe:
    def __init__(self, name, ingredients, steps, cooking_time):
        self.name = name
        self.ingredients = ingredients
        self.steps = steps
        self.cooking_time = cooking_time

class AddRecipeWindow:
    def __init__(self, master, app_instance):
        self.master = master
        self.master.title("Add Recipe")
        self.master.configure(bg="#F5F5F5")  # Light gray background

        self.app_instance = app_instance

        self.label_name = tk.Label(self.master, text="Recipe Name:", bg="#F5F5F5")  # Light gray background
        self.label_name.pack()
        self.entry_name = tk.Entry(self.master, width=60)
        self.entry_name.pack()

        self.label_ingredients = tk.Label(self.master, text="Ingredients:", bg="#F5F5F5")  # Light gray background
        self.label_ingredients.pack()
        self.entry_ingredients = tk.Text(self.master, width=60, height=5)
        self.entry_ingredients.pack()

        self.label_steps = tk.Label(self.master, text="Preparation Steps:", bg="#F5F5F5")  # Light gray background
        self.label_steps.pack()
        self.entry_steps = tk.Text(self.master, width=60, height=10)
        self.entry_steps.pack()

        self.label_cooking_time = tk.Label(self.master, text="Cooking Time:", bg="#F5F5F5")  # Light gray background
        self.label_cooking_time.pack()
        self.entry_cooking_time = tk.Entry(self.master, width=60)
        self.entry_cooking_time.pack()

        self.btn_add = tk.Button(self.master, text="Add Recipe", command=self.add_recipe, bg="#4CAF50", fg="white")  # Green button
        self.btn_add.pack()

    def add_recipe(self):
        name = self.entry_name.get()
        ingredients = self.entry_ingredients.get("1.0", tk.END).strip()
        steps = self.entry_steps.get("1.0", tk.END).strip()
        cooking_time = self.entry_cooking_time.get()

        if name and ingredients and steps and cooking_time:
            recipe = Recipe(name, ingredients, steps, cooking_time)
            self.app_instance.recipe_list.append(recipe)
            self.app_instance.recipe_display.insert(tk.END, name)
            self.master.destroy()
            messagebox.showinfo("Success", "Recipe added successfully!")
        else:
            messagebox.showwarning("Warning", "Please fill in all fields.")

class SearchWindow:
    def __init__(self, master, recipe_list):
        self.master = master
        self.master.title("Search Recipes")

        self.recipe_list = recipe_list

        self.label_search = tk.Label(self.master, text="Enter keyword to search:")
        self.label_search.pack()

        self.entry_search = tk.Entry(self.master, width=40)
        self.entry_search.pack()

        self.btn_search = tk.Button(self.master, text="Search", command=self.search_recipe,bg="#FF5722", fg="white")
        self.btn_search.pack()

        self.result_display = tk.Listbox(self.master, width=60, height=15)
        self.result_display.pack()

    def search_recipe(self):
        keyword = self.entry_search.get()
        if keyword:
            matching_recipes = [recipe.name for recipe in self.recipe_list if keyword.lower() in recipe.name.lower()]
            self.result_display.delete(0, tk.END)
            for recipe_name in matching_recipes:
                self.result_display.insert(tk.END, recipe_name)
        else:
            messagebox.showwarning("Warning", "Please enter a keyword to search.")

class RecipeManagerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Recipe Manager")
        self.master.configure(bg="#E0E0E0")  # Lighter gray background

        self.recipe_list = []

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="Welcome to Recipe Manager", bg="#E0E0E0", font=("Arial", 16)).pack(pady=20)  # Larger font and padding

        self.btn_add_recipe = tk.Button(self.master, text="Add Recipe", command=self.open_add_recipe_window, bg="#4CAF50", fg="white")  # Green button
        self.btn_add_recipe.pack()

        self.btn_search = tk.Button(self.master, text="Search", command=self.open_search_window, bg="#2196F3", fg="white")  # Blue button
        self.btn_search.pack()

        self.recipe_display = tk.Listbox(self.master, width=60, height=15)
        self.recipe_display.pack()

        self.btn_view = tk.Button(self.master, text="View Recipe Details", command=self.view_recipe_details, bg="#FF5722", fg="white")  # Orange button
        self.btn_view.pack()

    def open_add_recipe_window(self):
        add_recipe_window = tk.Toplevel(self.master)
        add_recipe_window.title("Add Recipe")
        add_recipe_app = AddRecipeWindow(add_recipe_window, self)

    def open_search_window(self):
        search_window = tk.Toplevel(self.master)
        search_window.title("Search Recipes")
        search_app = SearchWindow(search_window, self.recipe_list)

    def view_recipe_details(self):
        selected_index = self.recipe_display.curselection()
        if selected_index:
            selected_recipe_name = self.recipe_display.get(selected_index)
            selected_recipe = next((recipe for recipe in self.recipe_list if recipe.name == selected_recipe_name), None)
            if selected_recipe:
                details_window = tk.Toplevel(self.master)
                details_window.title("Recipe Details")

                tk.Label(details_window, text=f"Name: {selected_recipe.name}").pack()
                tk.Label(details_window, text=f"Ingredients: {selected_recipe.ingredients}").pack()
                tk.Label(details_window, text=f"Steps: {selected_recipe.steps}").pack()
                tk.Label(details_window, text=f"Cooking Time: {selected_recipe.cooking_time}").pack()
            else:
                messagebox.showwarning("Warning", "Recipe details not found.")
        else:
            messagebox.showwarning("Warning", "Please select a recipe from the list.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RecipeManagerApp(root)
    root.mainloop()











