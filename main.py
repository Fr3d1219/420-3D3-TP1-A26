from modeles.prix import Prix
from views.dashboard import Dashboard


if __name__ == "__main__":
    application = Dashboard(Prix())
    application.mainloop()
