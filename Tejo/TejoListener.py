import PUJ_Ogre
import time
import Ogre.Bites as OgreBites

class TejoListener( PUJ_Ogre.BaseListener ):
    def __init__( self, root, app ):
        super( TejoListener, self ).__init__( root )
        self.m_app = app
    # end def

    # def mousePressed( self, evt ):
    #     self.m_app.throwTejo( )
    #     print( 'Mouse button pressed: ' + str( evt.button ) )
    #     return True

    def mousePressed(self, evt):
        self.mouse_down_time = time.time()
        print("Mouse down...")
        return True

    # Usuario suelta el mouse
    def mouseReleased(self, evt):
        if self.mouse_down_time is not None:
            duration = time.time() - self.mouse_down_time
            print(f"Mouse up! Duration: {duration:.3f} s")
            self.m_app.throwTejo(duration)  # 🔥 Enviamos la duración
            self.mouse_down_time = None
        return True
    # end def

    def keyPressed(self, evt):
        print(evt.keysym.sym)
        if evt.keysym.sym == 122: #z
            self.m_app.zoomIn()
        elif evt.keysym.sym == 120: #x
            self.m_app.zoomOut()
        elif evt.keysym.sym == 114: #r
            self.m_app.resetGame()
        elif evt.keysym.sym == 112: #p
            self.m_app.printScore()
        elif evt.keysym.sym == 108: #l
            self.m_app.lateralView()
        elif evt.keysym.sym == 109: #m
            self.m_app.togglePause()
        # bloquear WASD
        
        return super(TejoListener, self).keyPressed(evt)
# end class