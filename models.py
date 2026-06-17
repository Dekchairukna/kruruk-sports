from datetime import datetime, date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    avatar_url = db.Column(db.String(500))
    social_provider = db.Column(db.String(40))
    social_id = db.Column(db.String(255), index=True)
    last_login_at = db.Column(db.DateTime)
    role = db.Column(db.String(40), default="organization_admin", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    memberships = db.relationship("OrganizationMember", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_superadmin(self):
        return self.role == "superadmin"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Organization(db.Model):
    __tablename__ = "organizations"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(180), nullable=False)
    org_type = db.Column(db.String(80), nullable=False, default="โรงเรียน")
    logo = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    members = db.relationship("OrganizationMember", back_populates="organization", cascade="all, delete-orphan")
    events = db.relationship("Event", back_populates="organization", cascade="all, delete-orphan")
    subscriptions = db.relationship("OrganizationSubscription", back_populates="organization", cascade="all, delete-orphan")
    invoices = db.relationship("Invoice", back_populates="organization", cascade="all, delete-orphan")
    payment_transactions = db.relationship("PaymentTransaction", back_populates="organization", cascade="all, delete-orphan")


class OrganizationMember(db.Model):
    __tablename__ = "organization_members"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id"), nullable=False)
    role = db.Column(db.String(40), nullable=False, default="organization_admin")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="memberships")
    organization = db.relationship("Organization", back_populates="members")

    __table_args__ = (db.UniqueConstraint("user_id", "organization_id", name="uq_user_organization"),)




class SubscriptionPlan(db.Model):
    __tablename__ = "subscription_plans"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(40), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, default=0, nullable=False)
    currency = db.Column(db.String(10), default="THB", nullable=False)
    billing_period = db.Column(db.String(40), default="monthly", nullable=False)
    duration_days = db.Column(db.Integer, default=30, nullable=False)

    max_events = db.Column(db.Integer, default=1, nullable=False)              # -1 = ไม่จำกัด
    max_teams_per_event = db.Column(db.Integer, default=4, nullable=False)     # -1 = ไม่จำกัด
    max_athletes_per_event = db.Column(db.Integer, default=100, nullable=False)# -1 = ไม่จำกัด
    allow_live_board = db.Column(db.Boolean, default=False, nullable=False)
    allow_certificates = db.Column(db.Boolean, default=False, nullable=False)
    allow_reports_pdf = db.Column(db.Boolean, default=False, nullable=False)

    is_active = db.Column(db.Boolean, default=True, nullable=False)
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    subscriptions = db.relationship("OrganizationSubscription", back_populates="plan")

    def limit_text(self, value):
        return "ไม่จำกัด" if value is None or value < 0 else str(value)


class OrganizationSubscription(db.Model):
    __tablename__ = "organization_subscriptions"
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id"), nullable=False, index=True)
    plan_id = db.Column(db.Integer, db.ForeignKey("subscription_plans.id"), nullable=False, index=True)
    status = db.Column(db.String(40), default="active", nullable=False)  # active, pending_payment, expired, cancelled
    start_date = db.Column(db.Date, default=date.today, nullable=False)
    end_date = db.Column(db.Date)
    manual_payment_note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    organization = db.relationship("Organization", back_populates="subscriptions")
    plan = db.relationship("SubscriptionPlan", back_populates="subscriptions")
    invoices = db.relationship("Invoice", back_populates="subscription", cascade="all, delete-orphan")

    @property
    def is_current(self):
        if self.status != "active":
            return False
        if self.end_date and self.end_date < date.today():
            return False
        return True


class Invoice(db.Model):
    __tablename__ = "invoices"
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id"), nullable=False, index=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey("organization_subscriptions.id"), nullable=True, index=True)
    invoice_no = db.Column(db.String(80), unique=True, nullable=False, index=True)
    title = db.Column(db.String(180), default="Subscription Invoice", nullable=False)
    amount = db.Column(db.Float, default=0, nullable=False)
    currency = db.Column(db.String(10), default="THB", nullable=False)
    status = db.Column(db.String(40), default="unpaid", nullable=False)  # unpaid, paid, cancelled
    due_date = db.Column(db.Date)
    paid_at = db.Column(db.DateTime)
    payment_method = db.Column(db.String(80), default="manual")
    gateway_reference = db.Column(db.String(255))
    payment_url = db.Column(db.Text)
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    organization = db.relationship("Organization", back_populates="invoices")
    subscription = db.relationship("OrganizationSubscription", back_populates="invoices")
    transactions = db.relationship("PaymentTransaction", back_populates="invoice", cascade="all, delete-orphan")


class OAuthAccount(db.Model):
    __tablename__ = "oauth_accounts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    provider = db.Column(db.String(40), nullable=False, index=True)
    provider_user_id = db.Column(db.String(255), nullable=False, index=True)
    email = db.Column(db.String(255), index=True)
    name = db.Column(db.String(180))
    avatar_url = db.Column(db.String(500))
    access_token = db.Column(db.Text)
    refresh_token = db.Column(db.Text)
    token_expires_at = db.Column(db.DateTime)
    raw_profile = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("oauth_accounts", cascade="all, delete-orphan"))

    __table_args__ = (db.UniqueConstraint("provider", "provider_user_id", name="uq_oauth_provider_user"),)


class PaymentTransaction(db.Model):
    __tablename__ = "payment_transactions"
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id"), nullable=False, index=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoices.id"), nullable=False, index=True)
    gateway = db.Column(db.String(40), nullable=False, default="manual")  # manual, promptpay, stripe, omise
    amount = db.Column(db.Float, default=0, nullable=False)
    currency = db.Column(db.String(10), default="THB", nullable=False)
    status = db.Column(db.String(40), default="pending", nullable=False)  # pending, paid, failed, cancelled
    provider_reference = db.Column(db.String(255), index=True)
    checkout_url = db.Column(db.Text)
    qr_payload = db.Column(db.Text)
    note = db.Column(db.Text)
    raw_response = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    paid_at = db.Column(db.DateTime)

    organization = db.relationship("Organization", back_populates="payment_transactions")
    invoice = db.relationship("Invoice", back_populates="transactions")


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id"), nullable=False, index=True)
    name = db.Column(db.String(220), nullable=False)
    competition_year = db.Column(db.String(20))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    location = db.Column(db.String(255))
    logo = db.Column(db.String(255))
    theme_color = db.Column(db.String(20), default="#4f46e5")
    status = db.Column(db.String(40), nullable=False, default="draft")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    organization = db.relationship("Organization", back_populates="events")
    teams = db.relationship("Team", back_populates="event", cascade="all, delete-orphan")


class Team(db.Model):
    __tablename__ = "teams"
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False, index=True)
    name = db.Column(db.String(180), nullable=False)
    color_name = db.Column(db.String(80))
    color_hex = db.Column(db.String(20), default="#ef4444")
    logo = db.Column(db.String(255))
    flag = db.Column(db.String(255))
    motto = db.Column(db.String(255))
    access_code = db.Column(db.String(40), nullable=False, index=True)
    registration_open = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    event = db.relationship("Event", back_populates="teams")
    profile = db.relationship("TeamProfile", back_populates="team", uselist=False, cascade="all, delete-orphan")
    people = db.relationship("TeamPerson", back_populates="team", cascade="all, delete-orphan")
    files = db.relationship("TeamFile", back_populates="team", cascade="all, delete-orphan")
    athletes = db.relationship("Athlete", back_populates="team", cascade="all, delete-orphan")
    coaches = db.relationship("Coach", back_populates="team", cascade="all, delete-orphan")

    __table_args__ = (db.UniqueConstraint("event_id", "access_code", name="uq_team_code_per_event"),)


class TeamProfile(db.Model):
    __tablename__ = "team_profiles"
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False, unique=True, index=True)

    director_name = db.Column(db.String(180))
    director_photo = db.Column(db.String(255))
    deputy_directors = db.Column(db.Text)
    advisors = db.Column(db.Text)
    coaches_summary = db.Column(db.Text)

    parade_title = db.Column(db.String(220))
    parade_concept = db.Column(db.Text)
    parade_description = db.Column(db.Text)

    stand_leaders = db.Column(db.Text)
    stand_member_total = db.Column(db.Integer, default=0)
    stand_member_male = db.Column(db.Integer, default=0)
    stand_member_female = db.Column(db.Integer, default=0)

    cheerleader_summary = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    team = db.relationship("Team", back_populates="profile")


class TeamPerson(db.Model):
    __tablename__ = "team_people"
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False, index=True)
    section = db.Column(db.String(40), nullable=False, index=True)
    name = db.Column(db.String(180), nullable=False)
    role = db.Column(db.String(180))
    phone = db.Column(db.String(80))
    note = db.Column(db.Text)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    team = db.relationship("Team", back_populates="people")


class TeamFile(db.Model):
    __tablename__ = "team_files"
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False, index=True)
    section = db.Column(db.String(40), nullable=False, index=True)
    title = db.Column(db.String(180))
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255))
    file_type = db.Column(db.String(40))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    team = db.relationship("Team", back_populates="files")


class SportCategory(db.Model):
    __tablename__ = "sport_categories"
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    event = db.relationship("Event", backref=db.backref("sport_categories", cascade="all, delete-orphan"))
    sports = db.relationship("Sport", back_populates="category", cascade="all, delete-orphan")

    __table_args__ = (db.UniqueConstraint("event_id", "name", name="uq_sport_category_per_event"),)


class Sport(db.Model):
    __tablename__ = "sports"
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey("sport_categories.id"), index=True)
    name = db.Column(db.String(160), nullable=False)
    default_format = db.Column(db.String(60), default="ranking")
    # วิธีบันทึกผล: score_only, set_based, ranking, contest
    result_type = db.Column(db.String(30), default="score_only", nullable=False)
    max_sets = db.Column(db.Integer, default=0, nullable=False)
    points_per_set = db.Column(db.Integer, default=0, nullable=False)
    sets_to_win = db.Column(db.Integer, default=0, nullable=False)
    note = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    event = db.relationship("Event", backref=db.backref("sports", cascade="all, delete-orphan"))
    category = db.relationship("SportCategory", back_populates="sports")
    divisions = db.relationship("SportDivision", back_populates="sport", cascade="all, delete-orphan")

    __table_args__ = (db.UniqueConstraint("event_id", "name", name="uq_sport_name_per_event"),)


class SportDivision(db.Model):
    __tablename__ = "sport_divisions"
    id = db.Column(db.Integer, primary_key=True)
    sport_id = db.Column(db.Integer, db.ForeignKey("sports.id"), nullable=False, index=True)
    class_name = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(20), nullable=False, default="ชาย")
    competition_format = db.Column(db.String(60), nullable=False, default="ranking")
    # ค่าบันทึกผลเฉพาะรายการย่อย ถ้าเว้นจะใช้ค่าจากชนิดกีฬา
    result_type = db.Column(db.String(30), default="score_only", nullable=False)
    max_sets = db.Column(db.Integer, default=0, nullable=False)
    points_per_set = db.Column(db.Integer, default=0, nullable=False)
    sets_to_win = db.Column(db.Integer, default=0, nullable=False)
    max_athletes_per_team = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sport = db.relationship("Sport", back_populates="divisions")

    __table_args__ = (db.UniqueConstraint("sport_id", "class_name", "gender", name="uq_sport_division"),)

    @property
    def label(self):
        return f"{self.sport.name} / {self.class_name} / {self.gender}"


class Athlete(db.Model):
    __tablename__ = "athletes"
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False, index=True)
    full_name = db.Column(db.String(180), nullable=False)
    gender = db.Column(db.String(20), nullable=False, default="ชาย")
    grade_level = db.Column(db.String(80))
    classroom = db.Column(db.String(80))
    student_no = db.Column(db.String(80))
    phone = db.Column(db.String(80))
    photo = db.Column(db.String(255))
    status = db.Column(db.String(30), nullable=False, default="pending")
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    team = db.relationship("Team", back_populates="athletes")
    registrations = db.relationship("AthleteRegistration", back_populates="athlete", cascade="all, delete-orphan")


class AthleteRegistration(db.Model):
    __tablename__ = "athlete_registrations"
    id = db.Column(db.Integer, primary_key=True)
    athlete_id = db.Column(db.Integer, db.ForeignKey("athletes.id"), nullable=False, index=True)
    sport_name = db.Column(db.String(140), nullable=False)
    category_name = db.Column(db.String(120))
    gender = db.Column(db.String(20), default="ชาย")
    status = db.Column(db.String(30), nullable=False, default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    athlete = db.relationship("Athlete", back_populates="registrations")


class Coach(db.Model):
    __tablename__ = "coaches"
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False, index=True)
    full_name = db.Column(db.String(180), nullable=False)
    phone = db.Column(db.String(80))
    sport_responsibility = db.Column(db.String(255))
    status = db.Column(db.String(30), nullable=False, default="pending")
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    team = db.relationship("Team", back_populates="coaches")


class RoundRobinCompetition(db.Model):
    __tablename__ = "round_robin_competitions"
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False, index=True)
    sport_division_id = db.Column(db.Integer, db.ForeignKey("sport_divisions.id"), nullable=True, index=True)
    name = db.Column(db.String(220), nullable=False)
    num_groups = db.Column(db.Integer, default=1, nullable=False)
    win_points = db.Column(db.Integer, default=3, nullable=False)
    draw_points = db.Column(db.Integer, default=1, nullable=False)
    loss_points = db.Column(db.Integer, default=0, nullable=False)
    advance_per_group = db.Column(db.Integer, default=1, nullable=False)
    best_runnerup_count = db.Column(db.Integer, default=0, nullable=False)
    tiebreakers = db.Column(db.String(255), default="points,goal_diff,goals_for,head_to_head,wins")
    status = db.Column(db.String(40), default="draft", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    event = db.relationship("Event", backref=db.backref("round_robin_competitions", cascade="all, delete-orphan"))
    sport_division = db.relationship("SportDivision")
    groups = db.relationship("RoundRobinGroup", back_populates="competition", cascade="all, delete-orphan", order_by="RoundRobinGroup.sort_order")
    matches = db.relationship("RoundRobinMatch", back_populates="competition", cascade="all, delete-orphan")

    @property
    def tiebreaker_list(self):
        return [x.strip() for x in (self.tiebreakers or "").split(",") if x.strip()]


class RoundRobinGroup(db.Model):
    __tablename__ = "round_robin_groups"
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey("round_robin_competitions.id"), nullable=False, index=True)
    name = db.Column(db.String(20), nullable=False)
    sort_order = db.Column(db.Integer, default=0)

    competition = db.relationship("RoundRobinCompetition", back_populates="groups")
    group_teams = db.relationship("RoundRobinGroupTeam", back_populates="group", cascade="all, delete-orphan", order_by="RoundRobinGroupTeam.sort_order")


class RoundRobinGroupTeam(db.Model):
    __tablename__ = "round_robin_group_teams"
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("round_robin_groups.id"), nullable=False, index=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False, index=True)
    sort_order = db.Column(db.Integer, default=0)

    group = db.relationship("RoundRobinGroup", back_populates="group_teams")
    team = db.relationship("Team")

    __table_args__ = (db.UniqueConstraint("group_id", "team_id", name="uq_rr_group_team"),)


class RoundRobinMatch(db.Model):
    __tablename__ = "round_robin_matches"
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey("round_robin_competitions.id"), nullable=False, index=True)
    group_id = db.Column(db.Integer, db.ForeignKey("round_robin_groups.id"), nullable=False, index=True)
    round_no = db.Column(db.Integer, default=1)
    match_no = db.Column(db.Integer, default=1)
    team_a_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False)
    team_b_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False)
    score_a = db.Column(db.Integer)
    score_b = db.Column(db.Integer)
    set_a = db.Column(db.Integer)
    set_b = db.Column(db.Integer)
    set_scores = db.Column(db.Text)  # JSON: [{"a":25,"b":18}, ...]
    score_history = db.Column(db.Text)  # JSON point-by-point history from quick score UI
    point_diff = db.Column(db.Integer, default=0)
    status = db.Column(db.String(40), default="scheduled", nullable=False)
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    competition = db.relationship("RoundRobinCompetition", back_populates="matches")
    group = db.relationship("RoundRobinGroup")
    team_a = db.relationship("Team", foreign_keys=[team_a_id])
    team_b = db.relationship("Team", foreign_keys=[team_b_id])



class KnockoutCompetition(db.Model):
    __tablename__ = "knockout_competitions"
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False, index=True)
    sport_division_id = db.Column(db.Integer, db.ForeignKey("sport_divisions.id"), nullable=True, index=True)
    source_round_robin_id = db.Column(db.Integer, db.ForeignKey("round_robin_competitions.id"), nullable=True, index=True)
    name = db.Column(db.String(220), nullable=False)
    result_type = db.Column(db.String(30), default="score_only", nullable=False)
    max_sets = db.Column(db.Integer, default=0, nullable=False)
    points_per_set = db.Column(db.Integer, default=0, nullable=False)
    sets_to_win = db.Column(db.Integer, default=0, nullable=False)
    status = db.Column(db.String(40), nullable=False, default="draft")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    event = db.relationship("Event", backref=db.backref("knockout_competitions", cascade="all, delete-orphan"))
    sport_division = db.relationship("SportDivision")
    source_round_robin = db.relationship("RoundRobinCompetition")
    matches = db.relationship("KnockoutMatch", back_populates="competition", cascade="all, delete-orphan", order_by="(KnockoutMatch.round_no, KnockoutMatch.match_no)")


class KnockoutMatch(db.Model):
    __tablename__ = "knockout_matches"
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey("knockout_competitions.id"), nullable=False, index=True)
    round_no = db.Column(db.Integer, default=1, nullable=False)
    round_name = db.Column(db.String(80), nullable=False, default="รอบแรก")
    match_no = db.Column(db.Integer, default=1, nullable=False)
    team_a_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=True)
    team_b_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=True)
    score_a = db.Column(db.Integer)
    score_b = db.Column(db.Integer)
    set_a = db.Column(db.Integer)
    set_b = db.Column(db.Integer)
    set_scores = db.Column(db.Text)
    score_history = db.Column(db.Text)
    point_diff = db.Column(db.Integer, default=0)
    winner_team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=True)
    status = db.Column(db.String(40), nullable=False, default="scheduled")
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    competition = db.relationship("KnockoutCompetition", back_populates="matches")
    team_a = db.relationship("Team", foreign_keys=[team_a_id])
    team_b = db.relationship("Team", foreign_keys=[team_b_id])
    winner_team = db.relationship("Team", foreign_keys=[winner_team_id])


class RankingCompetition(db.Model):
    __tablename__ = "ranking_competitions"
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False, index=True)
    sport_division_id = db.Column(db.Integer, db.ForeignKey("sport_divisions.id"), nullable=True, index=True)
    name = db.Column(db.String(220), nullable=False)
    result_mode = db.Column(db.String(30), nullable=False, default="rank")  # rank, time, distance
    medal_gold_rank = db.Column(db.Integer, nullable=False, default=1)
    medal_silver_rank = db.Column(db.Integer, nullable=False, default=2)
    medal_bronze_rank = db.Column(db.Integer, nullable=False, default=3)
    status = db.Column(db.String(40), nullable=False, default="draft")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    event = db.relationship("Event", backref=db.backref("ranking_competitions", cascade="all, delete-orphan"))
    sport_division = db.relationship("SportDivision")
    results = db.relationship("RankingResult", back_populates="competition", cascade="all, delete-orphan", order_by="RankingResult.rank")


class RankingResult(db.Model):
    __tablename__ = "ranking_results"
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey("ranking_competitions.id"), nullable=False, index=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False, index=True)
    athlete_id = db.Column(db.Integer, db.ForeignKey("athletes.id"), nullable=True, index=True)
    competitor_name = db.Column(db.String(180))
    rank = db.Column(db.Integer)
    time_value = db.Column(db.String(80))
    distance_value = db.Column(db.String(80))
    score_value = db.Column(db.String(80))
    medal = db.Column(db.String(20))
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    competition = db.relationship("RankingCompetition", back_populates="results")
    team = db.relationship("Team")
    athlete = db.relationship("Athlete")


class ContestCompetition(db.Model):
    __tablename__ = "contest_competitions"
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False, index=True)
    sport_division_id = db.Column(db.Integer, db.ForeignKey("sport_divisions.id"), nullable=True, index=True)
    name = db.Column(db.String(220), nullable=False)
    activity_type = db.Column(db.String(120), default="กิจกรรมประกวด")
    status = db.Column(db.String(40), nullable=False, default="draft")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    event = db.relationship("Event", backref=db.backref("contest_competitions", cascade="all, delete-orphan"))
    sport_division = db.relationship("SportDivision")
    criteria = db.relationship("ContestCriterion", back_populates="competition", cascade="all, delete-orphan", order_by="ContestCriterion.sort_order")
    judges = db.relationship("ContestJudge", back_populates="competition", cascade="all, delete-orphan", order_by="ContestJudge.id")
    scores = db.relationship("ContestScore", back_populates="competition", cascade="all, delete-orphan")
    results = db.relationship("ContestResult", back_populates="competition", cascade="all, delete-orphan", order_by="ContestResult.rank")


class ContestCriterion(db.Model):
    __tablename__ = "contest_criteria"
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey("contest_competitions.id"), nullable=False, index=True)
    name = db.Column(db.String(180), nullable=False)
    max_score = db.Column(db.Float, default=100, nullable=False)
    sort_order = db.Column(db.Integer, default=0)

    competition = db.relationship("ContestCompetition", back_populates="criteria")


class ContestJudge(db.Model):
    __tablename__ = "contest_judges"
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey("contest_competitions.id"), nullable=False, index=True)
    name = db.Column(db.String(180), nullable=False)
    position = db.Column(db.String(180))

    competition = db.relationship("ContestCompetition", back_populates="judges")


class ContestScore(db.Model):
    __tablename__ = "contest_scores"
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey("contest_competitions.id"), nullable=False, index=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False, index=True)
    criterion_id = db.Column(db.Integer, db.ForeignKey("contest_criteria.id"), nullable=False, index=True)
    judge_id = db.Column(db.Integer, db.ForeignKey("contest_judges.id"), nullable=False, index=True)
    score = db.Column(db.Float, default=0, nullable=False)
    note = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    competition = db.relationship("ContestCompetition", back_populates="scores")
    team = db.relationship("Team")
    criterion = db.relationship("ContestCriterion")
    judge = db.relationship("ContestJudge")

    __table_args__ = (db.UniqueConstraint("competition_id", "team_id", "criterion_id", "judge_id", name="uq_contest_score_cell"),)


class ContestResult(db.Model):
    __tablename__ = "contest_results"
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey("contest_competitions.id"), nullable=False, index=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False, index=True)
    total_score = db.Column(db.Float, default=0, nullable=False)
    rank = db.Column(db.Integer)
    medal = db.Column(db.String(20))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    competition = db.relationship("ContestCompetition", back_populates="results")
    team = db.relationship("Team")

    __table_args__ = (db.UniqueConstraint("competition_id", "team_id", name="uq_contest_result_team"),)


class CertificateTemplate(db.Model):
    __tablename__ = "certificate_templates"
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False, index=True)
    name = db.Column(db.String(180), nullable=False)
    cert_type = db.Column(db.String(40), nullable=False, default="participant")
    title = db.Column(db.String(180), default="เกียรติบัตร")
    subtitle = db.Column(db.String(255), default="ขอมอบเกียรติบัตรฉบับนี้ไว้เพื่อแสดงว่า")
    body = db.Column(db.Text, default="ได้เข้าร่วมกิจกรรม/การแข่งขันในงาน {event_name}")
    footer_text = db.Column(db.String(255))
    logo = db.Column(db.String(255))
    signature_left = db.Column(db.String(255))
    signature_left_name = db.Column(db.String(180))
    signature_left_position = db.Column(db.String(180))
    signature_right = db.Column(db.String(255))
    signature_right_name = db.Column(db.String(180))
    signature_right_position = db.Column(db.String(180))
    background_color = db.Column(db.String(20), default="#ffffff")
    accent_color = db.Column(db.String(20), default="#1d4ed8")
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    event = db.relationship("Event", backref=db.backref("certificate_templates", cascade="all, delete-orphan"))
    recipients = db.relationship("CertificateRecipient", back_populates="template", cascade="all, delete-orphan")


class CertificateRecipient(db.Model):
    __tablename__ = "certificate_recipients"
    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey("certificate_templates.id"), nullable=False, index=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False, index=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=True, index=True)
    athlete_id = db.Column(db.Integer, db.ForeignKey("athletes.id"), nullable=True, index=True)
    coach_id = db.Column(db.Integer, db.ForeignKey("coaches.id"), nullable=True, index=True)
    recipient_type = db.Column(db.String(40), nullable=False, default="manual")
    full_name = db.Column(db.String(180), nullable=False)
    role_text = db.Column(db.String(180))
    award_text = db.Column(db.String(255))
    sport_text = db.Column(db.String(255))
    verify_code = db.Column(db.String(40), nullable=False, unique=True, index=True)
    issued_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_revoked = db.Column(db.Boolean, default=False, nullable=False)

    template = db.relationship("CertificateTemplate", back_populates="recipients")
    event = db.relationship("Event")
    team = db.relationship("Team")
    athlete = db.relationship("Athlete")
    coach = db.relationship("Coach")

    @property
    def public_url_path(self):
        return f"/certificates/verify/{self.verify_code}"


class LiveBoardSetting(db.Model):
    __tablename__ = "live_board_settings"
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False, unique=True, index=True)
    marquee_text = db.Column(db.Text)
    theme = db.Column(db.String(40), default="stadium", nullable=False)
    refresh_seconds = db.Column(db.Integer, default=10, nullable=False)
    show_medals = db.Column(db.Boolean, default=True, nullable=False)
    show_schedule = db.Column(db.Boolean, default=True, nullable=False)
    show_results = db.Column(db.Boolean, default=True, nullable=False)
    show_rr_standings = db.Column(db.Boolean, default=True, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    event = db.relationship("Event", backref=db.backref("live_board_setting", uselist=False, cascade="all, delete-orphan"))
