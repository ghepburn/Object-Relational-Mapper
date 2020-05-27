class Subject:
	subscribers = []

	@classmethod
	def get_subscribers(cls):
		return cls.subscribers

	@classmethod
	def notify_subscribers(cls, *args):
		results = []
		if len(cls.subscribers) > 0:
			for subscriber in cls.subscribers:
				results.append(subscriber._notify(*args))
		return results

	@classmethod
	def subscribe(cls, subscriber):
		cls.subscribers.append(subscriber)