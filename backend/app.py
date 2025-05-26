from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
import enum
from sqlalchemy import event
from sqlalchemy.engine import Engine
from datetime import datetime

Base = declarative_base()

class EnrollmentType(enum.Enum):
    COURSE = "COURSE"
    PROGRAM = "PROGRAM"
    EXTERNAL = "EXTERNAL"

class EnrollmentState(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    COMPLETED = "COMPLETED"

class TopicState(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DELETED = "DELETED"

class EntryState(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DELETED = "DELETED"

class UserState(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DELETED = "DELETED"
    REGISTERED = "REGISTERED"

class Enrollment(Base):
    __tablename__ = 'enrollment'
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.course_id'), primary_key=True)
    enrollment_type = Column(Enum(EnrollmentType), nullable=False)
    enrollment_state = Column(Enum(EnrollmentState), nullable=False)

    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

class Topic(Base):
    __tablename__ = 'topics'
    topic_id = Column(Integer, primary_key=True)
    topic_title = Column(String(255), nullable=False)
    topic_content = Column(String, nullable=False)
    topic_created_at = Column(DateTime, default=datetime.utcnow)
    topic_deleted_at = Column(DateTime)
    topic_state = Column(Enum(TopicState), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.course_id'), nullable=False)
    topic_posted_by_user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)

    course = relationship("Course", back_populates="topics")
    user = relationship("User", back_populates="topics")
    entries = relationship("Entry", back_populates="topic")

class Entry(Base):
    __tablename__ = 'entries'
    entry_id = Column(Integer, primary_key=True)
    entry_content = Column(String, nullable=False)
    entry_created_at = Column(DateTime, default=datetime.utcnow)
    entry_deleted_at = Column(DateTime)
    entry_state = Column(Enum(EntryState), nullable=False)
    entry_parent_id = Column(Integer)
    entry_posted_by_user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    topic_id = Column(Integer, ForeignKey('topics.topic_id'), nullable=False)

    user = relationship("User", back_populates="entries")
    topic = relationship("Topic", back_populates="entries")

class Login(Base):
    __tablename__ = 'login'
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    user_login_id = Column(String(255), nullable=False)

    user = relationship("User", back_populates="login")

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(255), nullable=False)
    user_created_at = Column(DateTime, default=datetime.utcnow)
    user_deleted_at = Column(DateTime)
    user_state = Column(Enum(UserState), nullable=False)

    enrollments = relationship("Enrollment", back_populates="user")
    topics = relationship("Topic", back_populates="user")
    entries = relationship("Entry", back_populates="user")
    login = relationship("Login", back_populates="user", uselist=False)

class Course(Base):
    __tablename__ = 'courses'
    course_id = Column(Integer, primary_key=True)
    semester = Column(String(255), nullable=False)
    course_code = Column(String(255), nullable=False)
    course_name = Column(String(255), nullable=False)
    course_created_at = Column(DateTime, default=datetime.utcnow)

    enrollments = relationship("Enrollment", back_populates="course")
    topics = relationship("Topic", back_populates="course")

import pandas as pd
import numpy as np
from sqlalchemy.orm import sessionmaker

def read_excel_file(path):
    try:
        df = pd.read_excel(path)
        return df
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

courses_df = read_excel_file("data/courses.xlsx")

if courses_df is not None:
    print(courses_df.head())

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/courses')
def get_courses():
    if courses_df is not None:
        return jsonify(courses_df.replace(np.nan, None).to_dict(orient='records'))
    else:
        return jsonify({'message': 'No courses data available'}), 500

@app.route('/users')
def get_users():
    users_df = read_excel_file("data/users.xlsx")
    if users_df is not None:
        return jsonify(users_df.replace(np.nan, None).to_dict(orient='records'))
    else:
        return jsonify({'message': 'No users data available'}), 500

@app.route('/topics')
def get_topics():
    topics_df = read_excel_file("data/topics.xlsx")
    if topics_df is not None:
        return jsonify(topics_df.replace(np.nan, None).to_dict(orient='records'))
    else:
        return jsonify({'message': 'No topics data available'}), 500

@app.route('/entries')
def get_entries():
    entries_df = read_excel_file("data/entries.xlsx")
    if entries_df is not None:
        return jsonify(entries_df.replace(np.nan, None).to_dict(orient='records'))
    else:
        return jsonify({'message': 'No entries data available'}), 500

from flask import request

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = session.query(User).filter_by(user_name=username).first()
    if user and user.login.user_login_id == password:
        return jsonify({'message': 'Login successful', 'user_id': user.user_id}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/user/<int:user_id>/stats')
def get_user_stats(user_id):
    user = session.query(User).filter_by(user_id=user_id).first()
    if user:
        enrollment_count = len(user.enrollments)
        topic_count = len(user.topics)
        entry_count = len(user.entries)
        return jsonify({
            'enrollment_count': enrollment_count,
            'topic_count': topic_count,
            'entry_count': entry_count
        }), 200
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/enrollment')
def get_enrollment():
    enrollment_df = read_excel_file("data/enrollment.xlsx")
    if enrollment_df is not None:
        return jsonify(enrollment_df.replace(np.nan, None).to_dict(orient='records'))
    else:
        return jsonify({'message': 'No enrollment data available'}), 500

@app.route('/my_courses/<int:user_id>')
def get_my_courses(user_id):
    # Query the database to get the courses the user is enrolled in
    enrollments = session.query(Enrollment).filter_by(user_id=user_id, enrollment_state=EnrollmentState.ACTIVE).all()
    print(enrollments[0].enrollment_type)
    # Create a list of courses
    my_courses = [{
        'course_name': enrollment.course.course_name,
        'course_code': enrollment.course.course_code,
        'enrollment_type': enrollment.enrollment_type.value if enrollment.enrollment_type else ''
    } for enrollment in enrollments]

    return jsonify(my_courses)

@app.route('/recent_activity/<int:user_id>')
def get_recent_activity(user_id):
    # Query the database to get the recent activity for the user
    enrollments = session.query(Enrollment).filter_by(user_id=user_id, enrollment_state=EnrollmentState.ACTIVE).all()

    # Create a list of recent activity
    recent_activity = []
    for enrollment in enrollments:
        for topic in enrollment.course.topics:
            entries = session.query(Entry).filter_by(topic_id=topic.topic_id).order_by(Entry.entry_created_at.desc()).limit(5).all()
            for entry in entries:
                recent_activity.append({
                    'topic_title': topic.topic_title,
                    'topic_content': topic.topic_content,
                    'entry_content': entry.entry_content,
                    'entry_created_at': entry.entry_created_at.isoformat()
                })

    return jsonify(recent_activity)

@app.route('/my_contributions/<int:user_id>')
def get_my_contributions(user_id):
    # Count the number of topics posted by the user
    topic_count = session.query(Topic).filter_by(topic_posted_by_user_id=user_id).count()

    # Count the number of entries made by the user
    entry_count = session.query(Entry).filter_by(entry_posted_by_user_id=user_id).count()

    return jsonify({
        'topic_count': topic_count,
        'entry_count': entry_count
    })

@app.route('/newest_courses')
def get_newest_courses():
    # Query the database to get the newest courses
    newest_courses = session.query(Course).order_by(Course.course_created_at.desc()).limit(10).all()

    # Create a list of newest courses
    newest_courses_list = [{
        'course_name': course.course_name,
        'course_code': course.course_code,
        'course_created_at': course.course_created_at.isoformat()
    } for course in newest_courses]

    return jsonify(newest_courses_list)

@app.route('/active_discussions')
def get_active_discussions():
    # Query the database to get the active discussions
    active_discussions = session.query(Topic, Entry).\
        join(Entry, Topic.topic_id == Entry.topic_id).\
        order_by(Entry.entry_created_at.desc()).\
        limit(10).all()

    # Create a list of active discussions
    active_discussions_list = [{
        'topic_title': topic.topic_title,
        'topic_content': topic.topic_content,
        'entry_created_at': entry.entry_created_at.isoformat()
    } for topic, entry in active_discussions]

    return jsonify(active_discussions_list)

# SQLite setup
engine = create_engine('sqlite:///./suss.db')

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Read the users.xlsx file
users_df = pd.read_excel('data/users.xlsx')

# Print the unique values in the user_state column
print(users_df['user_state'].unique())

# Function to load data from Excel and insert into the database
def load_data(file_path, model, dtype=None, enum_columns=None):
    df = pd.read_excel(file_path, dtype=dtype)
    df = df.dropna(axis=1, how='all')

    # Convert enum columns
    if enum_columns:
        for col, enum_class in enum_columns.items():
            df[col] = df[col].apply(lambda x: enum_class[x.upper()].value if pd.notnull(x) and x.upper() in enum_class.__members__ else None)

    df.to_sql(model.__tablename__, engine, if_exists='replace', index=False, dtype={col: String for col in enum_columns} if enum_columns else None)

# Load data from Excel files
load_data('data/courses.xlsx', Course)
load_data('data/users.xlsx', User, enum_columns={'user_state': UserState})
load_data('data/login.xlsx', Login)
load_data('data/topics.xlsx', Topic, enum_columns={'topic_state': TopicState})
load_data('data/entries.xlsx', Entry, enum_columns={'entry_state': EntryState})
load_data('data/enrollment.xlsx', Enrollment, enum_columns={'enrollment_type': EnrollmentType, 'enrollment_state': EnrollmentState})

# Commit the changes
session.commit()

# Test the implementation
users = session.query(User).all()
for user in users:
    print(f"User ID: {user.user_id}, User Name: {user.user_name}")

# Get the first user
first_user = session.query(User).first()

# Print the first user's credentials
if first_user:
    print(f"First User Username: {first_user.user_name}")
    print(f"First User Password: {first_user.login.user_login_id}")

# Close the session
session.close()

if __name__ == '__main__':
    app.run(debug=True)
