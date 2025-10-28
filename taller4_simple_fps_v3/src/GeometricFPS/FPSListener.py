import PUJ_Ogre

class FPSListener( PUJ_Ogre.BaseListener ):
    def __init__( self, root ):
        super( FPSListener, self ).__init__( root )
    # end def

    def mousePressed( self, evt ):
        print( 'Mouse button pressed: ' + str( evt.button ) )
        return True
    # end def
# end class