import java.util.Scanner;

public class LoginSeguro {

    // ── Constantes de seguridad ──────────────────────────────────
    private static final int    MIN_LENGTH  = 8;
    private static final int    MAX_INTENTOS = 3;

    // ── Punto de entrada ─────────────────────────────────────────
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Nombre de usuario: ");
        String usuario = sc.nextLine().trim();

        int intentosFallidos = 0;
        boolean accesoConcedido = false;

        while (intentosFallidos < MAX_INTENTOS) {
            System.out.print("Contraseña: ");
            String contrasena = sc.nextLine();

            if (validarContrasena(contrasena)) {
                accesoConcedido = true;
                System.out.println("✓ Acceso concedido. Bienvenido, " + usuario);
                break;
            } else {
                intentosFallidos++;
                int restantes = MAX_INTENTOS - intentosFallidos;
                if (restantes > 0) {
                    System.out.println("✗ Contraseña no válida. Intentos restantes: " + restantes);
                } else {
                    System.out.println("⛔ Cuenta bloqueada. Demasiados intentos fallidos.");
                }
            }
        }
        sc.close();
    }

    // ── Validación completa de contraseña ───────────────────────
    public static boolean validarContrasena(String pass) {
        if (pass == null || pass.length() < MIN_LENGTH) {
            System.out.println("  → Mínimo " + MIN_LENGTH + " caracteres requeridos.");
            return false;
        }

        boolean tieneNumero    = false;
        boolean tieneMayuscula = false;

        for (char c : pass.toCharArray()) {
            if (Character.isDigit(c))     tieneNumero    = true;
            if (Character.isUpperCase(c)) tieneMayuscula = true;
        }

        if (!tieneNumero) {
            System.out.println("  → La contraseña debe contener al menos un número.");
            return false;
        }
        if (!tieneMayuscula) {
            System.out.println("  → La contraseña debe contener al menos una letra mayúscula.");
            return false;
        }
        return true;
    }
}