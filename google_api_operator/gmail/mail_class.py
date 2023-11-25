class Mail:
  def __init__(self):
    self.id = None
    self.subject = None
    self.date = None
    self._from = None
    self._to = None
    self.body = []
    self.html = None
  def get_connected_body(self):
    return '\n'.join(self.body)

class Mail_list(list):
  def __init__(self):
    self.known_flag = False
