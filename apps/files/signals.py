from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver, Signal
from .models import File, History, Folder


restored_file = Signal()


@receiver(post_save, sender=File)
def file_save(sender, instance, created, **kwargs):
    if created:
        History.objects.create(
            action = "UPLOADED",
            description = f"Subiste un elemento: {instance.name}",
            author = instance.author,
            date = instance.creation_date,
            file = instance
        )


@receiver(post_delete, sender=File)
def file_delete(sender, instance, **kwargs):
    History.objects.create(
        action = "DELETED",
        description = f"Borraste un elemento: {instance.name}",
        author = instance.author
    )


@receiver(pre_save, sender=File)
def file_update(sender, instance, **kwargs):

    if getattr(instance, "_restoring", False):  # Si está restaurando, no ejecutar la lógica de edición
        return 
    
    if instance.id:
        old_file = File.objects.filter(id=instance.id).first()
        changes = []

        if old_file.name != instance.name:
            changes.append(f'Nombre: "{old_file.name}" → "{instance.name}"')
            
        if old_file.folder != instance.folder:
            changes.append(f'Carpeta: "{old_file.folder}" → "{instance.folder}"')

        if changes:
            description = " | ".join(changes)
            History.objects.create(
                action = 'EDITED',
                description = f'Se modificó el archivo "{old_file.name}". Cambios: {description}',
                author = instance.author,
                file = instance
            )

        else:
            History.objects.create(
                action = 'EDITED',
                description = f'Se modificó el archivo "{old_file.name}"',
                author = instance.author,
                file = instance
            )


@receiver(restored_file)
def file_restored(sender, instance, old_version, **kwargs):

    History.objects.create(
        action = "RESTORED",
        description = f"Restauraste el archivo: '{instance.name}' a su version {old_version}",
        author_id = instance.author.id,
        file = instance
    )



@receiver(post_save, sender=Folder)
def folder_save(sender, instance, created, **kwargs):
    if created:
        History.objects.create(
            action = "CREATED",
            description = f"Creaste una carpeta: {instance.name}",
            author = instance.author,
            date = instance.creation_date,
            folder = instance
        )


@receiver(post_delete, sender=Folder)
def folder_delete(sender, instance, **kwargs):
    History.objects.create(
        action = "DELETED",
        description = f"Borraste una carpeta: {instance.name}",
        author = instance.author
    )


@receiver(pre_save, sender=Folder)
def folder_update(sender, instance, **kwargs):
    if instance.id:
        old_folder = Folder.objects.filter(id=instance.id).first()
        changes = []

        if old_folder.name != instance.name:
            changes.append(f'Nombre: "{old_folder.name}" → "{instance.name}"')
            
        if old_folder.parent_folder != instance.parent_folder:
            changes.append(f'Carpeta: "{old_folder.parent_folder}" → "{instance.parent_folder}"')

        if changes:
            description = " | ".join(changes)
            History.objects.create(
                action = 'EDITED',
                description = f'Se modificó la carpeta "{old_folder.name}". Cambios: {description}',
                author = instance.author,
                folder = instance
            )

        else:
            History.objects.create(
                action = 'EDITED',
                description = f'Se modificó la carpeta "{old_folder.name}"',
                author = instance.author,
                folder = instance
            )






