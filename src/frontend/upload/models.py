from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.documents.blocks import DocumentChooserBlock

class CSVUploadPage(Page):
    intro = StreamField([
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('document', DocumentChooserBlock()),
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]