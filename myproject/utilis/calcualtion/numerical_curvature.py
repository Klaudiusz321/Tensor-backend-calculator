import numpy as np
import sympy as sp
from myproject.utilis.calcualtion.derivative import numeric_derivative, total_derivative
import plotly.graph_objects as go
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Ustaw backend niewymagający GUI

def generate_numerical_curvature(Scalar_Curvature, wspolrzedne, parametry, ranges, points_per_dim=50):
    try:
        print("\nAnaliza wejścia:")
        print("Scalar_Curvature:", Scalar_Curvature)
        print("Współrzędne:", [str(w) for w in wspolrzedne])
        print("Parametry:", [str(p) for p in parametry])

        def calculate_curvature_value(*coords):
            """Oblicza wartość krzywizny dla danych współrzędnych"""
            try:
                substitutions = {}
                # Upewnij się, że wszystkie współrzędne są podstawione, w tym 't'
                default_coords = list(wspolrzedne)
                if not any(str(coord) == 't' for coord in default_coords):
                    t_symbol = sp.Symbol('t', real=True)
                    default_coords.insert(0, t_symbol)
                else:
                    t_symbol = next(sym for sym in wspolrzedne if str(sym) == 't')

                # Podstawienie dla współrzędnych
                for coord, val in zip(default_coords, coords):
                    substitutions[coord] = float(val)  # Konwertujemy na float
                    # Dodajemy funkcje trygonometryczne dla theta
                    if 'theta' in str(coord):
                        substitutions[sp.sin(coord)] = float(np.sin(val))
                        substitutions[sp.cos(coord)] = float(np.cos(val))
                    elif 'phi' in str(coord):
                        substitutions[sp.sin(coord)] = float(np.sin(val))
                        substitutions[sp.cos(coord)] = float(np.cos(val))
                    elif 'chi' in str(coord):
                        substitutions[sp.Symbol('chi')] = float(val)

                # Dla współrzędnych, które nie zostały przekazane, ustaw domyślną wartość
                if len(coords) < len(default_coords):
                    substitutions[t_symbol] = 1.0

                # Podstawienie dla funkcji a(t) i jej pochodnych
                t_val = substitutions.get(t_symbol, 1.0)
                a_func = sp.Function('a')(t_symbol)
                
                # Obliczamy wartości funkcji i pochodnych
                a_val = float(np.cosh(t_val))
                da_val = float(np.sinh(t_val))
                dda_val = float(np.cosh(t_val))

                # Podstawiamy funkcję i jej pochodne
                substitutions[a_func] = a_val
                substitutions[sp.Derivative(a_func, t_symbol)] = da_val
                substitutions[sp.Derivative(a_func, t_symbol, 2)] = dda_val

                # Podstawienie dla 'k'
                k_symbol = sp.Symbol('k', real=True)
                if k_symbol in Scalar_Curvature.free_symbols:
                    substitutions[k_symbol] = 1.0

                print("\nPodstawienia przed obliczeniem:")
                for k, v in substitutions.items():
                    print(f"{k} -> {v}")

                # Najpierw wykonujemy podstawienia
                expr = Scalar_Curvature
                print("\nWyrażenie początkowe:", expr)
                
                # Wykonujemy podstawienia i obliczamy pochodne
                expr = expr.subs(substitutions)
                print("Po podstawieniu:", expr)
                
                expr = expr.doit()  # Wymuszamy obliczenie pochodnych
                print("Po doit():", expr)
                
                # Próbujemy uprościć
                expr = sp.simplify(expr)
                print("Po uproszczeniu:", expr)
                
                # Konwertujemy na wartość liczbową
                numeric_expr = expr.evalf()
                print("Po evalf():", numeric_expr)

                if numeric_expr.is_number:
                    result = float(numeric_expr)
                    print("Końcowy wynik:", result)
                    return result if np.isfinite(result) and abs(result) < 1e10 else 0.0
                else:
                    print("Wyrażenie nie jest liczbą:", numeric_expr)
                    return 0.0

            except Exception as e:
                print(f"Błąd w obliczeniach: {e}")
                print("Aktualne wyrażenie:", Scalar_Curvature)
                print("Podstawienia:", substitutions)
                return 0.0

        def get_coordinate_ranges():
            """Określa zakresy dla różnych typów współrzędnych"""
            ranges = []
            for coord in wspolrzedne:
                name = str(coord)
                if name == 't':
                    ranges.append([0, 2.0])
                elif name == 'chi':
                    ranges.append([-0.99, 0.99])  # unikamy k*chi^2 = 1
                elif name == 'theta':
                    ranges.append([1e-3, np.pi - 1e-3])
                elif name == 'phi':
                    ranges.append([0, 2*np.pi - 1e-3])
                else:
                    ranges.append([-1.0, 1.0])
            return ranges

        # Generujemy punkty
        coord_ranges = get_coordinate_ranges()
        grid_points = []
        for min_val, max_val in coord_ranges:
            grid_points.append(np.linspace(min_val, max_val, points_per_dim))
        
        # Tworzymy siatkę punktów
        mesh_grids = np.meshgrid(*grid_points)
        points = np.vstack([grid.flatten() for grid in mesh_grids]).T
        
        # Obliczamy wartości krzywizny
        curvature_values = []
        for point in points:
            value = calculate_curvature_value(*point)
            curvature_values.append(value)

        curvature_values = np.array(curvature_values)
        
        # Usuwamy wartości ekstremalne
        nonzero_values = curvature_values[np.abs(curvature_values) > 1e-10]
        if len(nonzero_values) > 0:
            percentile_5 = np.percentile(nonzero_values, 5)
            percentile_95 = np.percentile(nonzero_values, 95)
            curvature_values = np.clip(curvature_values, percentile_5, percentile_95)
            
            print(f"\nStatystyki krzywizny:")
            print(f"Min: {np.min(nonzero_values)}")
            print(f"Max: {np.max(nonzero_values)}")
            print(f"Średnia: {np.mean(nonzero_values)}")
            print(f"Mediana: {np.median(nonzero_values)}")

        result = {
            'points': points.tolist(),
            'values': curvature_values.tolist(),
            'ranges': coord_ranges,
            'coordinates': [str(coord) for coord in wspolrzedne]
        }

        def visualize_curvature(points, curvature_values, coordinates):
            """Wizualizuje krzywiznę używając Plotly i Matplotlib"""
            # Przekształcamy punkty na tablicę numpy
            points = np.array(points)
            curvature = np.array(curvature_values)

            # 1. Plotly visualization
            fig_plotly = go.Figure(data=[go.Scatter3d(
                x=points[:, 0],
                y=points[:, 1],
                z=curvature,
                mode='markers',
                marker=dict(
                    size=3,
                    color=curvature,
                    colorscale='Viridis',
                    colorbar=dict(title='Curvature')
                )
            )])

            fig_plotly.update_layout(
                title="3D Wykres Krzywizny (Plotly)",
                scene=dict(
                    xaxis_title=coordinates[0],
                    yaxis_title=coordinates[1],
                    zaxis_title='Curvature'
                )
            )

            # 2. Matplotlib visualization
            fig_mpl = plt.figure(figsize=(10, 8))
            ax = fig_mpl.add_subplot(111, projection='3d')
            sc = ax.scatter(points[:, 0], points[:, 1], curvature, 
                           c=curvature, cmap='viridis')
            plt.colorbar(sc, label='Curvature')
            ax.set_xlabel(coordinates[0])
            ax.set_ylabel(coordinates[1])
            ax.set_zlabel('Curvature')
            plt.title("3D Wykres Krzywizny (Matplotlib)")

            return fig_plotly, fig_mpl

        # Generujemy wykresy
        fig_plotly, fig_mpl = visualize_curvature(
            points, 
            curvature_values, 
            result['coordinates']
        )

        # Dodajemy wykresy do wyniku
        result['plotly_figure'] = fig_plotly
        result['matplotlib_figure'] = fig_mpl

        return result

    except Exception as e:
        print(f"\nBŁĄD w generate_numerical_curvature: {e}")
        import traceback
        traceback.print_exc()
        return None
