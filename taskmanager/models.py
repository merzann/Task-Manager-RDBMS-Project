from taskmanager import db


class Category(db.Model):
    """Schema for the Category model"""
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(
        db.String(25), unique=True, nullable=False
    )
    tasks = db.relationship(
        "Task",
        backref="category",
        cascade="all, delete",
        lazy=True
    )

    def __repr__(self):
        """Represent Category instance as a string"""
        return self.category_name


class Task(db.Model):
    """Schema for the Task model"""
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(
        db.String(50), unique=True, nullable=False
    )
    task_description = db.Column(db.Text, nullable=False)
    is_urgent = db.Column(
        db.Boolean, default=False, nullable=False
    )
    due_date = db.Column(db.Date, nullable=False)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("category.id", ondelete="CASCADE"),
        nullable=False
    )

    def __repr__(self):
        """Represent Task instance as a string"""
        return (
            f"#{self.id} - Task: {self.task_name} | Urgent: {self.is_urgent}"
        )
