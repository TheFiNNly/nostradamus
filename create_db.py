from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost/stats"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "stats"
    id = Column(Integer, primary_key=True)
    champ = Column(String)
    date = Column(String)
    team_1 = Column(String)
    team_1_goal = Column(String)
    team_1_xg = Column(String)
    team_1_corners = Column(String)
    team_1_fouls = Column(String)
    team_1_offside = Column(String)
    team_1_shots = Column(String)
    team_1_attacks = Column(String)
    team_1_possession = Column(String)
    team_1_red = Column(String)
    team_1_pass = Column(String)
    team_1_saves = Column(String)
    team_1_pass_acc = Column(String)
    team_1_tacking = Column(String)
    team_2 = Column(String)
    team_2_goal = Column(String)
    team_2_xg = Column(String)
    team_2_corners = Column(String)
    team_2_fouls = Column(String)
    team_2_offside = Column(String)
    team_2_shots = Column(String)
    team_2_attacks = Column(String)
    team_2_possession = Column(String)
    team_2_red = Column(String)
    team_2_pass = Column(String)
    team_2_saves = Column(String)
    team_2_pass_acc = Column(String)
    team_2_tacking = Column(String)


if __name__ == "__main__":
    Base.metadata.create_all(engine)

