from ._anvil_designer import Reset_passwordTemplate
from anvil import *
import anvil.server

class Reset_password(Reset_passwordTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
