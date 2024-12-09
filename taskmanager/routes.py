from flask import render_template, request, redirect, url_for, flash
from taskmanager import app, db
from taskmanager.models import Category, Task

@app.route("/")
def home():
    return render_template("tasks.html")


@app.route("/categories")
def categories():
    categories = list(Category.query.order_by(Category.category_name).all())
    return render_template("categories.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    try:
        if request.method == "POST":
            # Get the category name from the form
            category_name = request.form.get("category_name")
            
            # Validate that the category name is not empty
            if not category_name:
                flash("Category name cannot be empty.", "error")
                return render_template("add_category.html")
            
            # Check if the category name already exists in the database
            existing_category = Category.query.filter_by(category_name=category_name).first()
            if existing_category:
                flash("Category already exists. Please choose a different name.", "warning")
                return render_template("add_category.html")

            # Add the new category to the database
            category = Category(category_name=category_name)
            db.session.add(category)
            db.session.commit()

            # Show a success message and redirect
            flash("Category added successfully!", "success")
            return redirect(url_for("categories"))

        return render_template("add_category.html")
    except Exception as e:
        # Log the exception and show an error message
        app.logger.error(f"Error adding category: {e}")
        flash("An unexpected error occurred. Please try again later.", "error")
        return render_template("add_category.html")


@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    if request.method == "POST":
        category.category_name = request.form.get("category_name")
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("edit_category.html", category=category)