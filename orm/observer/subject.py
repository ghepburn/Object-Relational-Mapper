class Subject:

	@classmethod
	def get_subscribers(cls):
		return cls.subscribers

	@classmethod
	def notify_subscribers(cls, *args):
		results = []
		if len(cls.subscribers) > 0:
			for subscriber in cls.subscribers:
				data = subscriber._notify(*args)
				results.append(data)
		if len(results) == 1:
			results = results[0]
		return results

	@classmethod
	def subscribe(cls, subscriber):
		if subscriber not in cls.subscribers:
			cls.subscribers.append(subscriber)

	@classmethod
	def remove_subscribers(cls):
		cls.subscribers = []

