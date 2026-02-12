from django.db.models import Manager


class ChoiceManager(Manager):
    # for one playthrough
    def active(self):
        return self.filter(active=True)

    def unrejected(self):
        return self.filter(rejected=False)
