from django.db import models 
from .annotations import AnnotationsProblems
from open_problems.models import Reference

#Theory models to attach for a particular open problem. 
class Theory(models.Model):
    theory_id = models.AutoField(db_column='Theory_id', primary_key=True)  # Field name made lowercase.
    theorytitle = models.CharField(db_column='TheoryTitle', max_length=40, blank=True, null=True)  # Field name made lowercase.
    theorydesc = models.TextField(db_column='TheoryDesc', blank=True, null=True)  # Field name made lowercase.
    parent_t_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='children', blank=True)
# end of edit by Hamid
    class Meta:
        db_table = "Theory"
        db_table_comment = "A theory annotation describing and categorisingthe open problem"
    def __str__(self) -> str:
        return f"{self.theory_id}: {self.theorytitle}"


class TheoryProblem(AnnotationsProblems): 
    theory = models.ForeignKey(Theory, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f"{self.theory}: {self.open_problem} "
    class Meta:
        db_table_comment = "Relation table for each theory and open problem"

class TheoryReferences(models.Model):
    ref = models.OneToOneField(Reference, models.DO_NOTHING, db_column='Ref_id', primary_key=True)  # Field name made lowercase. The composite primary key (Ref_id, Theory_id) found, that is not supported. The first column is selected.
    theory = models.ForeignKey(Theory, models.DO_NOTHING, db_column='Theory_id', null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'theory_reference'
        unique_together = (('ref', 'theory'))