

class Subject:
	def __init__(self):
		self.subscribers = []

	def get_subscribers(self):
		return self.subscribers

	def notify_subscribers(self, *args):
		if len(self.subscribers) > 0:
			for subscriber in self.subscribers:
				subscriber._notify(*args)

	def subscribe(self, subscriber):
		self.subscribers.append(subscriber)


class Subscriber:
	def notify(self):
		pass