from django.contrib import admin

from open_problems.custom_admin_classes.open_problems_admin import OPAdmin
from open_problems.custom_admin_classes.submitted_problems_admin import (
    SubmittedProblemsAdmin,
)
from open_problems.custom_admin_classes.open_problems_references_admin import OpenProblemsReferencesAdmin
from open_problems.models.open_problems import (
    Contact,
    OpenProblems,
    ProblemReference,
    Reference,
    RelatedProblem,
    SubmittedProblems,
)
from open_problems.models.references import Journal, RefType

# Registering models to admin without class created.

admin.site.register(OpenProblems, OPAdmin)
admin.site.register(SubmittedProblems, SubmittedProblemsAdmin)
admin.site.register(RelatedProblem)
admin.site.register(Reference)
admin.site.register(Journal)
admin.site.register(RefType)
admin.site.register(Contact)
admin.site.register(ProblemReference, OpenProblemsReferencesAdmin)
