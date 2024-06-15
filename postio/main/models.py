from django.db import models

# Create your models here.
# model for packages that individual users want to send
class UserPackage(models.Model):
    name = models.CharField(max_length=200) # package name
    weight = models.IntegerField()          # package weight
    width = models.IntegerField()             # package width
    lenght = models.IntegerField()          # package lenght
    height = models.IntegerField()          # package height
    price = models.IntegerField()           # price calculated based upon weight, dimensions
    paid = models.BooleanField()            # check if package delivery was paid for
    package_id = models.AutoField(primary_key=True)  # adds id to package
    status = models.CharField(max_length=50)    # status of package (ready to ship, dispatched, awaiting currier, awaiting pickup, in warehouse, in transit, delivered)

    def update_status(self, new_status):
        self.status = new_status
        self.save()
    def __str__(self):
        return (f"Packege id {self.package_id}")
# model of postbox(paczkomat)

# model of deliveryman