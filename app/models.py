from sqlalchemy import create_engine, Column, BigInteger, Integer, String, DECIMAL, ForeignKey, TIMESTAMP, Boolean, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, class_mapper
from datetime import datetime, timedelta

Base = declarative_base()


class CalorieBase(Base):
    __abstract__ = True  # Indicates that this is a base class

    def to_dict(self):
        # Use SQLAlchemy's class_mapper to dynamically get columns
        columns = [c.key for c in class_mapper(self.__class__).columns]
        return {
            column: (getattr(self, column).isoformat() if isinstance(getattr(self, column), datetime) else getattr(self, column))
            for column in columns
        }


class User(CalorieBase):
    __tablename__ = 'Users'
    user_id = Column(BigInteger, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)


class Food(CalorieBase):
    __tablename__ = 'Foods'
    food_id = Column(BigInteger, primary_key=True)
    name = Column(String(100), nullable=False)
    calories_per_gram = Column(DECIMAL, nullable=False)
    macros = Column(JSON, nullable=False)
    replacement_id = Column(BigInteger, ForeignKey('Foods.food_id'))


class UnitConversion(CalorieBase):
    __tablename__ = 'UnitConversions'
    unit_id = Column(BigInteger, primary_key=True)
    unit_name = Column(String(50), nullable=False)
    grams_per_unit = Column(DECIMAL, nullable=False)


class Group(CalorieBase):
    __tablename__ = 'Groups'
    group_id = Column(BigInteger, primary_key=True)
    group_name = Column(String(100), nullable=False)
    owner_id = Column(BigInteger, ForeignKey('Users.user_id'))
    public_until = Column(TIMESTAMP, nullable=False)


class UserGroup(CalorieBase):
    __tablename__ = 'UserGroups'
    user_group_id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('Users.user_id'))
    group_id = Column(BigInteger, ForeignKey('Groups.group_id'))


class Meal(CalorieBase):
    __tablename__ = 'Meals'
    meal_id = Column(BigInteger, primary_key=True)
    name = Column(String(100), nullable=False)
    author_id = Column(BigInteger, ForeignKey('Users.user_id'))
    public = Column(Boolean, default=False, nullable=False)
    replacement_id = Column(BigInteger, ForeignKey('Meals.meal_id'))


class MealFood(CalorieBase):
    __tablename__ = 'MealFoods'
    meal_food_id = Column(BigInteger, primary_key=True)
    meal_id = Column(BigInteger, ForeignKey('Meals.meal_id'))
    food_id = Column(BigInteger, ForeignKey('Foods.food_id'))
    quantity_in_grams = Column(DECIMAL, nullable=False)


class GroupMeal(CalorieBase):
    __tablename__ = 'GroupMeals'
    group_meal_id = Column(BigInteger, primary_key=True)
    group_id = Column(BigInteger, ForeignKey('Groups.group_id'))
    meal_id = Column(BigInteger, ForeignKey('Meals.meal_id'))


class FoodLog(CalorieBase):
    __tablename__ = 'FoodLog'
    log_id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('Users.user_id'))
    food_id = Column(BigInteger, ForeignKey('Foods.food_id'))
    quantity_in_grams = Column(DECIMAL, nullable=False)
    log_time = Column(TIMESTAMP, nullable=False)
    meal_type = Column(Enum('SNACK', 'BREAKFAST', 'LUNCH', 'DINNER', name='meal_type_enum', create_type=False))


# You can then create an engine and create all tables
# engine = create_engine('postgresql://username:password@localhost/dbname')
# Base.metadata.create_all(engine)
