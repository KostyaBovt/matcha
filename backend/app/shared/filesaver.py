class FileSaver(object):

  def __init__(self):
    pass

  def save_file(self, value, name, extention, path):
    file = open(path + '/' + name + '.' + extention, 'w')
    file.write(value)
    file.close()

  def read_file(self, name, path):
  	file = open(path + '/' + name, 'r')
  	ret = file.read()
  	file.close()
  	return ret
