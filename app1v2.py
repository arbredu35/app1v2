import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import os

# Stockage des comptes
accounts = []

# Charger les comptes depuis le fichier texte
def load_accounts():
    if os.path.exists("accounts.txt"):
        with open("accounts.txt", "r") as f:
            for line in f:
                parts = line.strip().split(", ")
                if len(parts) == 4:
                    category = parts[0].split(": ")[1]
                    site = parts[1].split(": ")[1]
                    email = parts[2].split(": ")[1]
                    password = parts[3].split(": ")[1]
                    accounts.append({"category": category, "site": site, "email": email, "password": password})

# Fonction pour générer un mot de passe
def generate_password():
    length = 10
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    new_password = "".join(random.choices(characters, k=length))
    password_entry.delete(0, tk.END)  # Supprimer l'existant
    password_entry.insert(0, new_password)

# Sauvegarder un compte dans le fichier et l'application
def save_account():
    category = category_var.get()
    site = site_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    
    if category and site and email and password:
        account_info = {"category": category, "site": site, "email": email, "password": password}
        accounts.append(account_info)
        save_to_file(account_info)
        show_content("All")
    else:
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

def save_to_file(account_info):
    with open("accounts.txt", "a") as f:
        f.write(f"Category: {account_info['category']}, Site: {account_info['site']}, Email: {account_info['email']}, Password: {account_info['password']}\n")

# Supprimer un compte
def delete_account(index):
    confirm = messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer ce compte ?")
    if confirm:
        del accounts[index]
        with open("accounts.txt", "w") as f:
            for acc in accounts:
                f.write(f"Category: {acc['category']}, Site: {acc['site']}, Email: {acc['email']}, Password: {acc['password']}\n")
        show_content("All")

# Modifier un compte
def edit_account(index):
    account = accounts[index]

    def save_changes():
        new_category = edit_category_var.get()
        new_site = edit_site_entry.get()
        new_email = edit_email_entry.get()
        new_password = edit_password_entry.get()

        if new_category and new_site and new_email and new_password:
            account.update({
                "category": new_category,
                "site": new_site,
                "email": new_email,
                "password": new_password
            })
            with open("accounts.txt", "w") as f:
                for acc in accounts:
                    f.write(f"Category: {acc['category']}, Site: {acc['site']}, Email: {acc['email']}, Password: {acc['password']}\n")
            edit_window.destroy()
            show_content("All")
        else:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

    edit_window = tk.Toplevel(root)
    edit_window.title("Modifier un Compte")
    edit_window.geometry("400x300")
    edit_window.config(bg="#1e1e2f")

    tk.Label(edit_window, text="Modifier un Compte", bg="#1e1e2f", fg="white", font=("Arial", 12)).pack(pady=10)

    edit_category_var = tk.StringVar(value=account["category"])
    edit_category_dropdown = ttk.Combobox(edit_window, textvariable=edit_category_var, values=[
        "Bank Account", "Credit Card", "Computer Login", 
        "Entertainment", "Mail", "Secure Account", 
        "Social Network", "Web Login"
    ], state="readonly", width=30)
    edit_category_dropdown.pack(pady=5)

    edit_site_entry = tk.Entry(edit_window, width=35, bg="#2a2a40", fg="white", relief="flat")
    edit_site_entry.insert(0, account["site"])
    edit_site_entry.pack(pady=5)

    edit_email_entry = tk.Entry(edit_window, width=35, bg="#2a2a40", fg="white", relief="flat")
    edit_email_entry.insert(0, account["email"])
    edit_email_entry.pack(pady=5)

    edit_password_entry = tk.Entry(edit_window, width=35, bg="#2a2a40", fg="white", relief="flat")
    edit_password_entry.insert(0, account["password"])
    edit_password_entry.pack(pady=5)

    tk.Button(edit_window, text="Sauvegarder", bg="#2a2a40", fg="white", command=save_changes).pack(pady=10)

# Afficher les comptes dans l'onglet sélectionné
def show_content(option):
    for widget in main_frame.winfo_children():
        widget.destroy()

    if option == "New Account":
        tk.Label(main_frame, text="Ajouter un Nouveau Compte", bg="#1e1e2f", fg="white", font=("Arial", 12)).pack(pady=10)

        form_frame = tk.Frame(main_frame, bg="#1e1e2f")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Catégorie :", bg="#1e1e2f", fg="white", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        global category_var, site_entry, email_entry, password_entry

        category_var = tk.StringVar()
        category_dropdown = ttk.Combobox(form_frame, textvariable=category_var, values=[
            "Bank Account", "Credit Card", "Computer Login", 
            "Entertainment", "Mail", "Secure Account", 
            "Social Network", "Web Login"
        ], state="readonly", width=37)
        category_dropdown.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Nom du Site :", bg="#1e1e2f", fg="white", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        site_entry = tk.Entry(form_frame, width=40, bg="#2a2a40", fg="white", relief="flat")
        site_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Nom/Email :", bg="#1e1e2f", fg="white", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        email_entry = tk.Entry(form_frame, width=40, bg="#2a2a40", fg="white", relief="flat")
        email_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Mot de Passe :", bg="#1e1e2f", fg="white", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="e")
        password_entry = tk.Entry(form_frame, width=40, bg="#2a2a40", fg="white", relief="flat")
        password_entry.grid(row=3, column=1, padx=10, pady=5)

        generate_btn = tk.Button(form_frame, text="Générer", bg="#2a2a40", fg="white", relief="flat", command=generate_password)
        generate_btn.grid(row=3, column=2, padx=10, pady=5)

        save_btn = tk.Button(main_frame, text="Sauvegarder", bg="#2a2a40", fg="white", command=save_account)
        save_btn.pack(pady=10)
    else:
        tk.Label(main_frame, text=f"Comptes pour {option} :", bg="#1e1e2f", fg="white", font=("Arial", 12)).pack(pady=10)

        for index, account in enumerate(accounts):
            if option == "All" or account["category"] == option:
                frame = tk.Frame(main_frame, bg="#2a2a40", padx=10, pady=5)
                frame.pack(fill="x", pady=5)

                tk.Label(frame, text=account["site"], bg="#2a2a40", fg="white", font=("Arial", 12, "bold")).pack(side="left")
                tk.Label(frame, text=account["email"], bg="#2a2a40", fg="white", font=("Arial", 10)).pack(side="left", padx=10)

                show_password_btn = tk.Button(frame, text="Afficher", bg="#444", fg="white", relief="flat",
                                              command=lambda idx=index: messagebox.showinfo("Mot de Passe", accounts[idx]["password"]))
                show_password_btn.pack(side="right", padx=5)

                edit_btn = tk.Button(frame, text="Modifier", bg="#444", fg="white", relief="flat", command=lambda idx=index: edit_account(idx))
                edit_btn.pack(side="right", padx=5)

                delete_btn = tk.Button(frame, text="🗑️", bg="#1e1e2f", fg="white", relief="flat", command=lambda idx=index: delete_account(idx))
                delete_btn.pack(side="right", padx=5)

# Initialisation
root = tk.Tk()
root.title("Gestionnaire de Mots de Passe")
root.geometry("900x600")
root.config(bg="#1e1e2f")

load_accounts()

sidebar = tk.Frame(root, bg="#2a2a40", width=200)
sidebar.pack(side="left", fill="y")

tk.Label(sidebar, text="Accounts", bg="#2a2a40", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

categories = ["All", "Bank Account", "Credit Card", "Computer Login", 
              "Entertainment", "Mail", "Secure Account", "Social Network", "Web Login", "New Account"]
for category in categories:
    btn = tk.Button(sidebar, text=category, bg="#2a2a40", fg="white", relief="flat", anchor="w",
                    command=lambda cat=category: show_content(cat))
    btn.pack(fill="x", padx=10, pady=2)

main_frame = tk.Frame(root, bg="#1e1e2f")
main_frame.pack(fill="both", expand=True)

show_content("All")

root.mainloop()