// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================
#ifndef __PUJ_GL__Scene__h__
#define __PUJ_GL__Scene__h__

#include <PUJ_GL/Traits.h>
#include <PUJ_GL/Object.h>         // Asumiendo que existe (base para MeshObject, OrthoBase)
#include <PUJ_GL/MeshObject.h>     // Para MeshObject
#include <PUJ_GL/OrthoBase.h>      // Para OrthoBase
#include <PUJ_GL/ParametricModel.h> // Para TParametricFunction y ParametricModel
#include <PUJ_GL/Image.h>
#include <functional>              // Para std::function
#include <vector>
#include <string>

namespace PUJ_GL
{
  /**
   * Clase Scene para manejar objetos (meshes, modelos paramétricos, etc.).
   */
  class PUJ_GL_EXPORT Scene
  {
    PUJ_GL_Traits;

  public:
    using Self = Scene;
    using TObjectPtr = Object*;  // Raw pointer como en tu código original
    using TObjects = std::vector<TObjectPtr>;

    // Firma ACTUALIZADA de TParametricFunction (coincide con ParametricModel.h)
    using TParametricFunction = std::function< void(
      TReal* point, TReal* normal,
      TReal* du, TReal* dv,  // Derivadas parciales para cálculo de normales
      const TReal& u, const TReal& v
    ) >;

  public:
    Scene( );
    virtual ~Scene( );

    void draw( );
    const TReal* clear_color( ) const;
    const TReal* bounding_box( ) const;

    void load_mesh( const std::string& fname );
    void load_orthobase( const TReal& s );
    void load_parametric_model(
      TParametricFunction function,
      const TReal& minU, const TReal& maxU,
      const TNatural& samplesU, bool closedU,
      const TReal& minV, const TReal& maxV,
      const TNatural& samplesV, bool closedV,
      PUJ_GL::Image* image = nullptr
    );

    // Acceso al último objeto cargado (para setear materiales en App.cxx)
    MeshObject* get_last_object( ) const;

    // Reset (público para acceso externo si es necesario)
    void reset( );  // Renombrado de _reset para público

  protected:
    TObjects m_Objects;
    TReal m_Color[4] { 0.0f, 0.0f, 0.0f, 1.0f };  // Clear color (no mutable, no se modifica en const)

    // Cache para bounding box: mutable para permitir actualización en métodos const
    mutable TReal m_BoundingBox[6] { 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f };
    mutable bool m_BoundingBoxUpdated { false };

    void _reset( );  // Implementación privada
    void _update_bounding_box( );  // Declaración forward (implementa en .cxx si es necesario)
  };
} // end namespace

#endif // __PUJ_GL__Scene__h__
// eof - Scene.h
