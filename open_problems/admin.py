from django.contrib import admin

from open_problems.custom_admin_classes.open_problems_admin import OPAdmin
from open_problems.custom_admin_classes.open_problems_references_admin import (
    OpenProblemsReferencesAdmin,
)
from open_problems.custom_admin_classes.submitted_problems_admin import (
    SubmittedProblemsAdmin,
)
from open_problems.models import (
    Contact,
    OpenProblem,
    ProblemReference,
    RelatedProblem,
    SubmittedOpenProblem,
)

# Registering models to admin without class created.

admin.site.register(OpenProblem, OPAdmin)
admin.site.register(SubmittedOpenProblem, SubmittedProblemsAdmin)
admin.site.register(RelatedProblem)
admin.site.register(Contact)
admin.site.register(ProblemReference, OpenProblemsReferencesAdmin)
