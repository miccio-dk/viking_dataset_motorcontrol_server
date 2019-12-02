function result = motor_move(motor, direction, amount)
    import matlab.net.*
    import matlab.net.http.*

    r = RequestMessage;
    
    % request motor movement
    uri = URI(['http://localhost:5000/move/' motor '/' direction '/' num2str(amount)]);
    resp = send(r,uri);
    if(resp.StatusCode == 200)
        % wait until it's done
        while 1
            uri = URI(['http://localhost:5000/poll/' motor]);
            resp = send(r,uri);
            if(resp.StatusCode == 200)
                if(strcmp(resp.Body.Data, 'DONE') == 1)
                    result = true;
                    break
                end
            else
                result = false;
                break
            end
            pause(0.5)
        end
        
    else
        result = false;
    end
end
