from django.db import models


class JobInformation(models.Model):
    info_id = models.AutoField(primary_key=True)
    info_title = models.CharField(max_length=50)

    class Meta:
        abstract = True


class Organisation(JobInformation):
    def __str__(self) -> str:
        return f"{self.info_title}"


class JobField(JobInformation):
    def __str__(self) -> str:
        return f"{self.info_title}"


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    job_field = models.ForeignKey(
        JobField, on_delete=models.SET_NULL, null=True, blank=True
    )
    organisation = models.ForeignKey(
        Organisation, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        db_table = "Contact"
        db_table_comment = "This table contains the contact details of the person who submitted the question"

    def __str__(self):
        return f"{self.first_name} {self.last_name} : {self.email}"
