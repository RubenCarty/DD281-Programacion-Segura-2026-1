import java.util.Scanner;

public class LoginSeg {


    public void main() {

        Scanner sc = new Scanner(System.in);

        // Datos de simulación (puedes cambiarlos)
        final int MAX_INTENTOS = 3;
        int intentosFallidos = 0;
        boolean accesoConcedido = false;

        System.out.println("--- SISTEMA DE LOGIN SEGURO ---");

        // Bucle para controlar el bloqueo tras 3 intentos fallidos
        while (intentosFallidos < MAX_INTENTOS && !accesoConcedido) {
            System.out.println("\nIntento " + (intentosFallidos + 1) + " de " + MAX_INTENTOS + ":");

            // 1. Solicitar nombre de usuario
            System.out.print("Ingrese usuario: ");
            String usuario = sc.nextLine();

            // 2. Solicitar contraseña
            System.out.print("Ingrese contraseña: ");
            String password = sc.nextLine();

            // Variables de control de los requisitos
            boolean tieneNumero = false;
            boolean tieneMayuscula = false;
            boolean pasoValidaciones = true;

            // 3. Verificar longitud mínima de 8 caracteres
            if (password.length() < 8) {
                System.out.println("❌ Error: La contraseña debe tener al menos 8 caracteres.");
                pasoValidaciones = false;
            }

            // Evaluar carácter por carácter para buscar números y mayúsculas
            for (char c : password.toCharArray()) {
                if (Character.isDigit(c)) {
                    tieneNumero = true;
                }
                if (Character.isUpperCase(c)) {
                    tieneMayuscula = true;
                }
            }

            // 4. Verificar presencia de al menos un número
            if (!tieneNumero) {
                System.out.println("❌ Error: La contraseña debe contener al menos un número.");
                pasoValidaciones = false;
            }

            // 5. Verificar presencia de al menos una mayúscula
            if (!tieneMayuscula) {
                System.out.println("❌ Error: La contraseña debe contener al menos una letra mayúscula.");
                pasoValidaciones = false;
            }

            // Evaluar resultado del intento actual
            if (pasoValidaciones) {
                // 7. Si todo es válido: Acceso concedido
                System.out.println("\n✅ Acceso concedido. Bienvenido, " + usuario);
                accesoConcedido = true;
            } else {
                intentosFallidos++;
                System.out.println("⚠️ Credenciales inválidas.");
            }
        }

        // 8. Bloquear si supera los 3 intentos fallidos
        if (!accesoConcedido) {
            System.out.println("\n🚫 Sistema bloqueado: Ha superado los 3 intentos fallidos consecutivos.");
        }

    }
}
