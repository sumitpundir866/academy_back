from app.database.session import engine
from app.models.rbac_model import Base, User, Role, HierarchyLevel, StaffRank, ModuleMaster, Screens, RoleScreenMap, MstOrbat
from app.models.academy_models import ClassInfo, TeamMember, GalleryImage, AboutInfo, ContactInfo

def create_tables():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    create_tables()
