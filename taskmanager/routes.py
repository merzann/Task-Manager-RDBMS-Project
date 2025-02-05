from flask import (
    render_template, request, redirect, url_for, flash
)
from datetime import datetime
from taskmanager import app, db
from taskmanager.models import Category, Task


@app.route("/")
def home():
    tasks = list(Task.query.order_by(Task.id).all())
    return render_template("tasks.html", tasks=tasks)


@app.route("/categories")
def categories():
    categories = list(Category.query.order_by(Category.category_name).all())
    return render_template("categories.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    try:
        if request.method == "POST":
            category_name = request.form.get("category_name")

            if not category_name:
                flash("Category name cannot be empty.", "error")
                return render_template("add_category.html")

            existing_category = Category.query.filter_by(
                category_name=category_name
            ).first()

            if existing_category:
                flash(
                    "Category already exists. Please choose a different name.",
                    "warning",
                )
                return render_template("add_category.html")

            category = Category(category_name=category_name)
            db.session.add(category)
            db.session.commit()

            flash("Category added successfully!", "success")
            return redirect(url_for("categories"))

        return render_template("add_category.html")
    except Exception as e:
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


@app.route("/delete_category/<int:category_id>")
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for("categories"))


@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    try:
        categories = list(
            Category.query.order_by(
                Category.category_name
            ).all())
        if not categories:
            flash(
                "No categories found. Please add a category first.", "warning"
            )
            return redirect(url_for("add_category"))

        if request.method == "POST":
            task_name = request.form.get("task_name")
            if not task_name:
                flash("Task name cannot be empty.", "error")
                return render_template(
                    "add_task.html", categories=categories
                )

            task_description = request.form.get("task_description")
            is_urgent = bool(request.form.get("is_urgent"))
            due_date = request.form.get("due_date")
            category_id = request.form.get("category_id")

            if (
                not category_id
                or not category_id.isdigit()
                or not Category.query.get(category_id)
            ):
                flash(
                    "Invalid category selected. "
                    "Please choose a valid category.",
                    "error",
                )
                return render_template(
                    "add_task.html", categories=categories
                )

            if due_date:
                try:
                    parsed_date = datetime.strptime(due_date, "%d %B, %Y")
                    due_date = parsed_date.strftime("%Y-%m-%d")
                except ValueError:
                    flash(
                        "Invalid date format. Please use the datepicker.",
                        "error",
                    )
                    return render_template(
                        "add_task.html", categories=categories
                    )

            task = Task(
                task_name=task_name,
                task_description=task_description,
                is_urgent=is_urgent,
                due_date=due_date,
                category_id=int(category_id),
            )

            db.session.add(task)
            db.session.commit()
            flash("Task added successfully!", "success")
            return redirect(url_for("home"))

        return render_template("add_task.html", categories=categories)
    except Exception as e:
        app.logger.error(f"Error adding task: {e}")
        flash("An unexpected error occurred. Please try again later.", "error")
        return render_template("add_task.html", categories=categories)


@app.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    categories = list(Category.query.order_by(Category.category_name).all())

    if request.method == "POST":
        task.task_name = request.form.get("task_name")
        task.task_description = request.form.get("task_description")
        task.is_urgent = bool(request.form.get("is_urgent"))
        task.due_date = request.form.get("due_date")
        task.category_id = request.form.get("category_id")
        db.session.commit()

    return render_template(
        "edit_task.html", task=task, categories=categories
    )


@app.route("/delete_task/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("home"))
