import java.util.Scanner;

public class LoginSeguro {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        int intentosFallidos = 0;
        final int MAX_INTENTOS = 3;

        while (intentosFallidos < MAX_INTENTOS) {

            System.out.print("Ingrese nombre de usuario: ");
            String usuario = sc.nextLine();

            System.out.print("Ingrese contraseña: ");
            String password = sc.nextLine();

            // Validaciones estrictas de seguridad
            boolean longitudValida = password.length() >= 8;
            boolean tieneNumero = password.matches(".*[0-9].*");
            boolean tieneMayuscula = password.matches(".*[A-Z].*");

            if (!longitudValida) {

                System.out.println(
                    "Error: La contraseña debe tener al menos 8 caracteres."
                );

            } else if (!tieneNumero) {

                System.out.println(
                    "Error: La contraseña debe contener al menos un número."
                );

            } else if (!tieneMayuscula) {

                System.out.println(
                    "Error: La contraseña debe contener al menos una letra mayúscula."
                );

            } else {

                System.out.println(
                    "Acceso concedido. Bienvenido, " + usuario
                );
                break;
            }

            intentosFallidos++;

            if (intentosFallidos >= MAX_INTENTOS) {
                System.out.println(
                    "Cuenta bloqueada temporalmente tras 3 intentos fallidos."
                );
            }
        }

        sc.close();
    }
}