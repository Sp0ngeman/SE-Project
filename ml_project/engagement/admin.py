from django.contrib import admin
from .models import (
    TextbookSection, TextbookPage, TextbookSlide,
    RevisionQuestion, RevisionQuestionAttempt, RevisionQuestionAttemptDetail,
    WritingInteraction, UserSlideRead, UserSlideReadSession
)

@admin.register(TextbookSection)
class TextbookSectionAdmin(admin.ModelAdmin):
    list_display = ('id','section_title')
    search_fields = ('section_title',)

@admin.register(TextbookPage)
class TextbookPageAdmin(admin.ModelAdmin):
    list_display = ('id','page_title','get_sections')
    search_fields = ('page_title',)
    filter_horizontal = ('sections',)
    def get_sections(self, obj):
        return ", ".join([s.section_title for s in obj.sections.all()])
    get_sections.short_description = "Sections"

@admin.register(TextbookSlide)
class TextbookSlideAdmin(admin.ModelAdmin):
    list_display = ('id','slide_title','get_pages')
    search_fields = ('slide_title',)
    filter_horizontal = ('pages',)
    def get_pages(self, obj):
        return ", ".join([p.page_title for p in obj.pages.all()])
    get_pages.short_description = "Pages"

@admin.register(RevisionQuestion)
class RevisionQuestionAdmin(admin.ModelAdmin):
    list_display = ('id','textbook_page')
    list_filter = ('textbook_page',)

@admin.register(RevisionQuestionAttempt)
class RevisionQuestionAttemptAdmin(admin.ModelAdmin):
    list_display = ('id','user','question','viewed','correct','processed')
    list_filter = ('user','question','processed')

@admin.register(RevisionQuestionAttemptDetail)
class RevisionQuestionAttemptDetailAdmin(admin.ModelAdmin):
    list_display = ('id','attempt','is_correct','timestamp','processed')
    list_filter = ('is_correct','processed')

@admin.register(WritingInteraction)
class WritingInteractionAdmin(admin.ModelAdmin):
    list_display = ('id','user_id','page_id','grade','timestamp')
    search_fields = ('user_id','page_id')

@admin.register(UserSlideRead)
class UserSlideReadAdmin(admin.ModelAdmin):
    list_display = ('id','user','slide','slide_status')
    list_filter = ('slide_status',)

@admin.register(UserSlideReadSession)
class UserSlideReadSessionAdmin(admin.ModelAdmin):
    list_display = ('id','slide_read','expanded','collapsed','read')
    list_filter = ('expanded','collapsed','read')
