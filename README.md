# LockBox

**LockBox** es un sistema de almacenamiento de archivos diseñado exclusivamente para uso personal, con un enfoque en la seguridad y el control de versiones. Este proyecto permite gestionar archivos de manera eficiente, asegurando que cada cambio realizado en los archivos esté documentado y sea fácilmente reversible.

## Descripción

LockBox es una solución pensada para quienes necesitan mantener un registro completo de versiones de sus archivos. Integrado con **Google Cloud Storage**, ofrece una manera sencilla y segura de almacenar, acceder y gestionar archivos, manteniendo un historial claro de todas las modificaciones.

## Características

- **Control de versiones**: Cada archivo guardado en LockBox tiene un historial completo de cambios, lo que permite revertir a versiones anteriores en cualquier momento.
- **Seguridad**: Todos los archivos se almacenan de manera segura en Google Cloud Storage, asegurando una alta disponibilidad y protección contra pérdida de datos.
- **Historial de modificaciones**: Además del control de versiones, LockBox mantiene un registro detallado de las modificaciones realizadas en los archivos, incluyendo quién y cuándo se hicieron los cambios.

## ¿Por qué LockBox?

- **Fiabilidad**: Basado en Google Cloud Storage, LockBox garantiza un almacenamiento confiable y accesible desde cualquier lugar.
- **Gestión de versiones**: Ideal para quienes necesitan un control preciso sobre la evolución de sus archivos.
- **Sin necesidad de configuraciones complejas**: El sistema está configurado para trabajar exclusivamente con Google Cloud Storage, sin la necesidad de elegir o gestionar otros servicios de almacenamiento.

## Cómo empezar

1. **Configura Google Cloud Storage**: Asegúrate de tener una cuenta en Google Cloud y configura un bucket de almacenamiento.
2. **Instala las dependencias**: Ejecuta el comando `pip install -r requirements.txt` para instalar las dependencias necesarias.
3. **Configura el acceso**: Añade las credenciales de Google Cloud a tu entorno para que LockBox pueda acceder a tu almacenamiento.
4. **Usa el sistema**: Agrega, modifica y consulta tus archivos con el control de versiones incorporado.

## Tecnologías utilizadas

- **Google Cloud Storage**: Para almacenamiento seguro y eficiente.
- **Python**: Lenguaje principal para el desarrollo.
- **Django/Django-REST-Framework**: Framework utilizado para el backend.
- **PostgreSQL**: Base de datos utilizada

## Contribuciones

Este proyecto está destinado exclusivamente para uso personal, pero si deseas colaborar o mejorar el proyecto, puedes realizar un fork y enviar un pull request.

