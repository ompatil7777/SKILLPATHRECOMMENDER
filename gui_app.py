# gui_app.py (replace existing file with this)
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# Ensure project root is on sys.path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Set Django settings module - change this line if your settings module name differs
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillpath_project.settings')

import django
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from recommender.models import Domain, Skill, Career, UserProfile
from recommender.recommendation_engine import RecommendationEngine

class SkillPathApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SkillPath Recommender")
        self.root.geometry("980x680")

        # Layout frames
        self.top = ttk.Frame(root, padding=6)
        self.top.pack(fill='x')
        self.body = ttk.Frame(root, padding=10)
        self.body.pack(fill='both', expand=True)
        self.debug = ttk.Frame(root, padding=6)
        self.debug.pack(fill='x')

        # Debug text
        self.debug_box = tk.Text(self.debug, height=6)
        self.debug_box.pack(fill='x')
        self.log("GUI starting...")

        # state
        self.current_user = None
        self.username_entry = None
        self.password_entry = None

        self.show_login_screen()

    def log(self, *parts):
        msg = " ".join(map(str, parts))
        print("DEBUG:", msg)
        try:
            self.debug_box.insert('end', msg + "\n")
            self.debug_box.see('end')
        except Exception:
            pass

    def clear_body(self):
        for w in self.body.winfo_children():
            w.destroy()

    # --- Login / Register ---
    def show_login_screen(self):
        self.clear_body()
        self.log("Render login screen")
        ttk.Label(self.top, text="SkillPath Recommender", font=('Segoe UI', 16, 'bold')).pack(pady=4)

        frm = ttk.Frame(self.body, padding=12)
        frm.pack(pady=20)

        ttk.Label(frm, text="Username:").grid(row=0, column=0, padx=6, pady=6, sticky='e')
        self.username_entry = ttk.Entry(frm, width=36)
        self.username_entry.grid(row=0, column=1, padx=6, pady=6)

        ttk.Label(frm, text="Password:").grid(row=1, column=0, padx=6, pady=6, sticky='e')
        self.password_entry = ttk.Entry(frm, width=36, show='*')
        self.password_entry.grid(row=1, column=1, padx=6, pady=6)

        btns = ttk.Frame(self.body)
        btns.pack(pady=8)
        ttk.Button(btns, text="Login", command=self.login).pack(side='left', padx=6)
        ttk.Button(btns, text="Register", command=self.register).pack(side='left', padx=6)

    def login(self):
        username = (self.username_entry.get() or "").strip()
        password = (self.password_entry.get() or "").strip()
        self.log("Attempt login:", username)

        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return

        try:
            user = authenticate(username=username, password=password)
        except Exception as e:
            self.log("authenticate error:", e)
            messagebox.showerror("Error", f"Authentication error: {e}")
            return

        if user:
            self.current_user = user
            UserProfile.objects.get_or_create(user=user)
            self.log("Login success:", username)
            self.show_main_menu()
            return

        # deeper check to diagnose
        u = User.objects.filter(username=username).first()
        if not u:
            messagebox.showerror("Error", "User not found")
            self.log("User not found in DB:", username)
            return
        ok = u.check_password(password)
        self.log("User exists, check_password:", ok)
        if ok:
            # fallback
            self.current_user = u
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Invalid password")

    def register(self):
        username = (self.username_entry.get() or "").strip()
        password = (self.password_entry.get() or "").strip()
        self.log("Register attempt:", username)

        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        if len(password) < 4:
            messagebox.showerror("Error", "Password must be at least 4 chars")
            return
        if User.objects.filter(username=username).exists():
            messagebox.showerror("Error", "Username already exists")
            return

        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.get_or_create(user=user)
        messagebox.showinfo("Success", "Registered. Please login.")
        self.username_entry.delete(0, 'end'); self.password_entry.delete(0, 'end')

    # --- Main menu ---
    def show_main_menu(self):
        try:
            self.clear_body()
            if not self.current_user:
                messagebox.showwarning("Not logged in", "Please login first")
                self.show_login_screen()
                return
            self.log("Render main menu for", self.current_user.username)

            ttk.Label(self.body, text=f"Welcome, {self.current_user.username}", font=('Segoe UI', 14, 'bold')).pack(pady=8)
            menu_box = ttk.Frame(self.body, padding=12)
            menu_box.pack(pady=12)

            ttk.Button(menu_box, text="Setup Profile", width=30, command=self.show_profile_setup).pack(pady=6)
            ttk.Button(menu_box, text="Get Recommendations", width=30, command=self.show_recommendations).pack(pady=6)
            ttk.Button(menu_box, text="Learning Path", width=30, command=self.show_learning_path).pack(pady=6)
            ttk.Button(menu_box, text="Explore Skills", width=30, command=self.show_skill_explorer).pack(pady=6)
            ttk.Button(menu_box, text="Logout", width=30, command=self.logout).pack(pady=6)

        except Exception as e:
            tb = traceback.format_exc()
            self.log("Error in show_main_menu:", e)
            self.clear_body()
            ttk.Label(self.body, text="Error rendering menu", font=('Segoe UI', 14, 'bold')).pack(pady=6)
            t = scrolledtext.ScrolledText(self.body, height=12); t.pack(fill='both', expand=True, padx=10, pady=10)
            t.insert('end', str(e) + "\n\n" + tb)
            t.configure(state='disabled')
            ttk.Button(self.body, text="Back to Login", command=self.show_login_screen).pack(pady=8)

    def logout(self):
        self.log("Logout user:", getattr(self.current_user, 'username', None))
        self.current_user = None
        self.show_login_screen()

    # --- Profile setup ---
    def show_profile_setup(self):
        self.clear_body()
        ttk.Label(self.body, text="Setup Profile", font=('Segoe UI', 14, 'bold')).pack(pady=6)

        domain_names = [d.name for d in Domain.objects.all()]
        domain_var = tk.StringVar(value=domain_names[0] if domain_names else "")
        ttk.Label(self.body, text="Select domain:").pack(anchor='w', padx=10)
        cmb = ttk.Combobox(self.body, values=domain_names, textvariable=domain_var, width=48)
        cmb.pack(padx=10, pady=6)

        skills_list = tk.Listbox(self.body, selectmode='extended', height=8)
        skills_list.pack(padx=10, pady=6, fill='x')

        def load_skills(e=None):
            skills_list.delete(0, 'end')
            d = Domain.objects.filter(name=domain_var.get()).first()
            if d:
                for s in d.skills.all():
                    skills_list.insert('end', s.name)
        cmb.bind("<<ComboboxSelected>>", load_skills)
        load_skills()

        def save_profile():
            d = Domain.objects.filter(name=domain_var.get()).first()
            profile, _ = UserProfile.objects.get_or_create(user=self.current_user)
            profile.domain = d
            profile.save()
            profile.skills.clear()
            for i in skills_list.curselection():
                name = skills_list.get(i)
                s = Skill.objects.filter(name=name, domain=d).first()
                if s:
                    profile.skills.add(s)
            profile.save()
            messagebox.showinfo("Saved", "Profile saved")
            self.show_main_menu()

        ttk.Button(self.body, text="Save Profile", command=save_profile).pack(pady=8)
        ttk.Button(self.body, text="Back", command=self.show_main_menu).pack(pady=6)

    # --- Recommendations ---
    def show_recommendations(self):
        self.clear_body()
        ttk.Label(self.body, text="Career Recommendations", font=('Segoe UI', 14, 'bold')).pack(pady=6)
        txt = scrolledtext.ScrolledText(self.body, height=18)
        txt.pack(fill='both', expand=True, padx=8, pady=6)

        profile = UserProfile.objects.filter(user=self.current_user).first()
        if not profile or not profile.domain:
            txt.insert('end', "No profile or domain set. Please setup profile.\n")
            txt.configure(state='disabled')
            ttk.Button(self.body, text="Back", command=self.show_main_menu).pack(pady=8)
            return

        domain = profile.domain
        skills = list(profile.skills.all())
        results = RecommendationEngine.get_matching_careers(domain, skills)
        if not results:
            txt.insert('end', "No matching careers found.\n")
        else:
            for i, r in enumerate(results, start=1):
                c = r['career']
                txt.insert('end', f"{i}. {c.title} ({c.domain.name})\n")
                txt.insert('end', f"   Score {r['score']:.2f} - {r['matching_skills']}/{r['total_required']}\n")
                if getattr(c, 'average_salary', None):
                    txt.insert('end', f"   Salary: {c.average_salary}\n")
                txt.insert('end', f"   {c.description}\n\n")
        txt.configure(state='disabled')
        ttk.Button(self.body, text="Back", command=self.show_main_menu).pack(pady=8)

    # --- Learning path ---
    def show_learning_path(self):
        self.clear_body()
        ttk.Label(self.body, text="Learning Path", font=('Segoe UI', 14, 'bold')).pack(pady=6)
        txt = scrolledtext.ScrolledText(self.body, height=18)
        txt.pack(fill='both', expand=True, padx=8, pady=6)

        profile = UserProfile.objects.filter(user=self.current_user).first()
        if not profile or not profile.domain:
            txt.insert('end', "No profile/domain. Set up profile first.\n")
            txt.configure(state='disabled')
            ttk.Button(self.body, text="Back", command=self.show_main_menu).pack(pady=8)
            return

        results = RecommendationEngine.get_matching_careers(profile.domain, list(profile.skills.all()))
        if not results:
            txt.insert('end', "No career recommendations to build a path.\n")
            txt.configure(state='disabled')
            ttk.Button(self.body, text="Back", command=self.show_main_menu).pack(pady=8)
            return

        top = results[0]['career']
        txt.insert('end', f"Top career: {top.title}\n\n")
        path = RecommendationEngine.generate_learning_path(top, list(profile.skills.all()))
        if not path:
            txt.insert('end', "No path generated.\n")
        else:
            for i, step in enumerate(path, start=1):
                name = getattr(step, 'name', str(step))
                level = getattr(step, 'difficulty_level', '')
                txt.insert('end', f"{i}. {name} — {level}\n")
                try:
                    prereqs = step.prerequisites.all()
                except Exception:
                    prereqs = []
                if prereqs:
                    txt.insert('end', "    Prereqs: " + ", ".join([p.name for p in prereqs]) + "\n")
                txt.insert('end', "\n")
        txt.configure(state='disabled')
        ttk.Button(self.body, text="Back", command=self.show_main_menu).pack(pady=8)

    # --- Skill explorer ---
    def show_skill_explorer(self):
        self.clear_body()
        ttk.Label(self.body, text="Skill Explorer", font=('Segoe UI', 14, 'bold')).pack(pady=6)
        names = [d.name for d in Domain.objects.all()]
        var = tk.StringVar(value=names[0] if names else "")
        cmb = ttk.Combobox(self.body, values=names, textvariable=var)
        cmb.pack(pady=6)
        txt = scrolledtext.ScrolledText(self.body, height=16)
        txt.pack(fill='both', expand=True, padx=8, pady=6)

        def show(_=None):
            txt.configure(state='normal'); txt.delete('1.0','end')
            d = Domain.objects.filter(name=var.get()).first()
            if not d:
                txt.insert('end', 'No domain selected\n')
            else:
                for s in d.skills.all():
                    txt.insert('end', f"{s.name} — {s.difficulty_level}\n")
                    if s.prerequisites.exists():
                        txt.insert('end', "    Prereqs: " + ", ".join([p.name for p in s.prerequisites.all()]) + "\n")
                    txt.insert('end', "\n")
            txt.configure(state='disabled')
        cmb.bind("<<ComboboxSelected>>", show)
        show()
        ttk.Button(self.body, text="Back", command=self.show_main_menu).pack(pady=8)

if __name__ == "__main__":
    root = tk.Tk()
    app = SkillPathApp(root)
    root.mainloop()
