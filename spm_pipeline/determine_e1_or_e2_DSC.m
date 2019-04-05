function type = determine_e1_or_e2_DSC(file_name)
    for i = 1:length(file_name)-1
        if file_name(i) == 'e'
            if file_name(i+1) == '1'
                type = 'e1';
                return;
            elseif file_name(i+1) == '2'
                type = 'e2';
                return;
            else
                type = 'None';
                return;
            end
        end
    end
end