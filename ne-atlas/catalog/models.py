from django.db import models

class College(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)  # CT, ME, MA, NH, RI, VT
    institution_type = models.CharField(
        max_length=30,
        choices=[
            ("public", "Public"),
            ("private", "Private nonprofit"),
            ("for_profit", "Private for-profit"),
        ],
    )

    def __str__(self):
        return f"{self.name} ({self.state})"

class Program(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name="programs")
    name = models.CharField(max_length=255)
    degree_level = models.CharField(
        max_length=20,
        choices=[
            ("associate", "Associate"),
            ("bachelor", "Bachelor"),
            ("master", "Master"),
            ("certificate", "Certificate"),
        ],
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("current", "Current"),
            ("former", "Former"),
        ],
        default="current",
    )

    def __str__(self):
        return f"{self.name} — {self.college.name}"

class ProgramYear(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="years")
    academic_year = models.CharField(max_length=9)  # e.g. 2016-2026
    enrollment = models.PositiveIntegerField()
    completions = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("program", "academic_year")
        ordering = ["academic_year"]

    def __str__(self):
        return f"{self.program.name} {self.academic_year}"