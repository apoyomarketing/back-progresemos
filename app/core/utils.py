from django.utils.text import slugify


def unique_slugify(instance, value, slug_field_name="slug", max_length=50):
    base_slug = slugify(value)[:max_length]
    slug = base_slug
    counter = 2

    qs = instance.__class__._default_manager.all()
    if instance.pk:
        qs = qs.exclude(pk=instance.pk)

    while qs.filter(**{slug_field_name: slug}).exists():
        suffix = f"-{counter}"
        slug = f"{base_slug[:max_length - len(suffix)]}{suffix}"
        counter += 1

    return slug
