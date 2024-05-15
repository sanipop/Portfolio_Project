# Importing necessary modules and objects from the market module.
from market import db, login_manager
from market import bcrypt

# Importing UserMixin for user authentication.
from flask_login import UserMixin

# Function to load a user by ID for login management.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Model class for User, inheriting from db.Model and UserMixin.
class User(db.Model, UserMixin):
    # Database columns for user ID, username, email address, password hash, budget, and items.
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)
  
    # Property to format budget for display.
    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f"{self.budget}$"
          
    
    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
      
    # Method to check if the password is correct.
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
      
    # Method to check if the user can purchase an item.
    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price
      
    # Method to check if the user can sell an item.
    def can_sell(self, item_obj):
        return item_obj in self.items

# Model class for Item, representing items in the market.
class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    # Representation method for item objects.  
    def __repr__(self):
        return f'Item {self.name}'
      
    # Method to handle item purchase by a user.
    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()
      
    # Method to handle item sale by a user.
    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()
